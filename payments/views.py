from django.shortcuts import render

# views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import razorpay
from generate.models import Project
from .models import Payment, LiveUsagePlan
from generate.models import ExpiredProject
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


GRACE_DAYS = 5

PLAN_DURATIONS = {
    "1_month": timedelta(days=30),
    "6_months": timedelta(days=182),
    "12_months": timedelta(days=365),
}


class RazorpayOrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    PLAN_PRICING = {
        "1_month": Decimal("499.00"),
        "6_months": Decimal("2799.00"),
        "12_months": Decimal("4999.00"),
    }

    def post(self, request, project_slug=None):
        plan = request.data.get("plan")
        if plan not in self.PLAN_PRICING:
            raise ValidationError({"plan": "Invalid plan selected"})

        # If project_slug is provided, get that project
        if project_slug:
            project = get_object_or_404(Project, slug=project_slug, user=request.user)
        else:
            # Pick first project of the user if no slug provided
            projects = Project.objects.filter(user=request.user)
            if not projects.exists():
                raise ValidationError({"project": "No project found for user"})
            project = projects.first()

        amount = self.PLAN_PRICING[plan]

        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": int(amount * 100),  # in paise
            "currency": "INR",
            "payment_capture": "1"
        })

        # Create Payment record with status "created"
        Payment.objects.create(
            paid_by=request.user,   # audit only
            project=project,
            payment_for="live",
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            plan=plan,
            status="created"
        )


        return Response({
            "order_id": razorpay_order["id"],
            "amount": int(amount * 100),
            "currency": "INR",
            "plan": plan,
            "project_slug": project.slug,
            "project_name": project.project_name
        })

from django.db import transaction
from generate.models import ProjectVersion, BeforeDeployLiveAppData
from django.core.exceptions import ValidationError

def first_time_or_after_expiry_promote_preview_to_live(project):
    # 1️⃣ FIRST: check if LIVE exists
    live = ProjectVersion.objects.filter(
        project=project,
        version_type="live"
    ).first()

    if live:
        # 🔴 LIVE already exists → leave everything
        return live

    # 2️⃣ No LIVE → check expiry
    expired_snapshot = ExpiredProject.objects.filter(
        project=project
    ).first()

    if expired_snapshot:
        # 🟡 Restore expired snapshot into LIVE
        live = ProjectVersion.objects.create(
            project=project,
            version_type="live",
            ui_schema=expired_snapshot.ui_schema,
            workflows=expired_snapshot.workflows,
            data_types=expired_snapshot.data_types,
            app_data=expired_snapshot.live_app_data,
        )

        expired_snapshot.delete()
        return live

    # 3️⃣ No LIVE, no expiry → FIRST TIME DEPLOY
    preview = ProjectVersion.objects.filter(
        project=project,
        version_type="preview"
    ).first()

    if not preview:
        raise ValidationError("No preview version found")

    before_deploy_obj = BeforeDeployLiveAppData.objects.filter(
        project=project
    ).first()

    live = ProjectVersion.objects.create(
        project=project,
        version_type="live",
        ui_schema=preview.ui_schema,
        workflows=preview.workflows,
        data_types=preview.data_types,
        app_data=before_deploy_obj.data if before_deploy_obj else {},
    )

    if before_deploy_obj:
        before_deploy_obj.delete()

    return live


class RazorpayPaymentCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_slug):
        project = get_object_or_404(Project, slug=project_slug, user=request.user)

        razorpay_order_id = request.data.get("razorpayOrderId")
        razorpay_payment_id = request.data.get("razorpayPaymentId")
        razorpay_signature = request.data.get("razorpaySignature")

        # 1️⃣ Required data check
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response(
                {"error": "Missing payment data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment = get_object_or_404(
            Payment,
            razorpay_order_id=razorpay_order_id,
            status="created"
        )

        plan = payment.plan   # ✅ TRUSTED SOURCE
        project = payment.project

        # 2️⃣ Plan validation
        if plan not in RazorpayOrderCreateAPIView.PLAN_PRICING:
            return Response(
                {"error": "Invalid plan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Idempotency check
        existing_payment = Payment.objects.filter(
            razorpay_order_id=razorpay_order_id,
            status="paid"
        ).first()

        if existing_payment:
            return Response(
                {"message": "Payment already processed"},
                status=status.HTTP_200_OK
            )


        # 4️⃣ Signature verification
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5️⃣ Atomic DB write
        with transaction.atomic():
            # Update existing "created" payment
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = "paid"
            payment.save()



            now = timezone.now()

            # Get last subscription (active or expired)
            last_plan = LiveUsagePlan.objects.filter(
                project=project
            ).order_by("-expires_at").first()

            if not last_plan:
                # 🟢 First purchase
                started_at = now

            else:
                expiry = last_plan.expires_at
                grace_end = expiry + timedelta(days=GRACE_DAYS)

                if now <= expiry:
                    # 🟢 Renew before expiry (addon)
                    started_at = expiry

                elif expiry < now <= grace_end:
                    # Renew during grace → resume from next day
                    started_at = expiry + timedelta(days=1)

                else:
                    # Renew after grace → start fresh
                    started_at = now

            # Final expiry calculation
            expires_at = started_at + PLAN_DURATIONS[plan]

            # Create new subscription record
            live_plan = LiveUsagePlan.objects.create(
                project=project,
                payment=payment,
                plan=plan,
                started_at=started_at,
                expires_at=expires_at
            )


            # 🔥 PROMOTE PREVIEW → LIVE
            live_version = first_time_or_after_expiry_promote_preview_to_live(project)

        return Response({
            "message": "Payment successful",
            "live_plan": {
                "plan": live_plan.plan,
                "expires_at": live_plan.expires_at
            },
            "live_version_updated_at": live_version.updated_at
        })

class PlatformUsageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usage, _ = PlatformUsage.objects.get_or_create(user=request.user)

        free_left = max(
            0,
            usage.FREE_PROMPT_LIMIT - usage.free_prompts_used
        )

        return Response({
            "free_left": free_left,
            "paid_left": usage.paid_prompt_credits,
            "total_left": free_left + usage.paid_prompt_credits
        })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from payments.models import Payment, PlatformUsage
import razorpay

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreatePlatformOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan = request.data.get("plan")  # starter / pro

        pack = Payment.PLATFORM_PROMPT_PACKS.get(plan)
        if not pack:
            return Response({"error": "Invalid platform plan"}, status=400)

        amount = pack["amount"]
        credits = pack["credits"]

        # 1️⃣ Create Razorpay order
        order = razorpay_client.order.create({
            "amount": amount * 100,  # paise
            "currency": "INR",
            "payment_capture": 1,
        })

        # 2️⃣ Create payment record (platform)
        Payment.objects.create(
            paid_by=request.user,
            payment_for="platform",
            razorpay_order_id=order["id"],
            amount=amount,
            currency="INR",
            prompt_credits=credits,
            status="created",
        )

        return Response({
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "credits": credits,
        })

from rest_framework.exceptions import ValidationError


class CompletePlatformPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("razorpayOrderId")
        payment_id = request.data.get("razorpayPaymentId")
        signature = request.data.get("razorpaySignature")

        if not all([order_id, payment_id, signature]):
            return Response({"error": "Missing payment fields"}, status=400)

        # 1️⃣ Verify signature
        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid payment signature"}, status=400)

        # 2️⃣ Fetch payment
        try:
            payment = Payment.objects.get(
                razorpay_order_id=order_id,
                payment_for="platform",
                status="created"
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        # 3️⃣ Mark payment success
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "paid"
        payment.save()

        # 4️⃣ Add credits to PlatformUsage
        usage, _ = PlatformUsage.objects.get_or_create(user=payment.paid_by)
        usage.paid_prompt_credits += payment.prompt_credits
        usage.save(update_fields=["paid_prompt_credits"])

        return Response({
            "message": "Platform credits added successfully",
            "credits_added": payment.prompt_credits,
            "total_paid_credits": usage.paid_prompt_credits,
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from generate.models import Project, ProjectVersion

from django.utils import timezone

from django.core.exceptions import ValidationError

def update_live_from_preview(project):
    """
    Update an existing Live version:
    - Take structure (schema, workflows, datatypes) from Preview version
    - Keep app_data from existing Live version
    """
    # 1️⃣ Get Preview version
    preview = ProjectVersion.objects.filter(
        project=project,
        version_type="preview"
    ).first()

    if not preview:
        raise ValidationError("No preview version found")

    # 2️⃣ Get Live version (must exist)
    live_version = ProjectVersion.objects.filter(
        project=project,
        version_type="live"
    ).first()

    if not live_version:
        raise ValidationError("No deployed Live version found")

    # 3️⃣ Update only the structure
    live_version.ui_schema = preview.ui_schema
    live_version.workflows = preview.workflows
    live_version.data_types = preview.data_types
    # ⚡ Keep existing live app_data untouched

    live_version.save(update_fields=["ui_schema", "workflows", "data_types", "updated_at"])

    return live_version

from generate.services import rename_live_tables_and_fields

class UpdateLiveProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_slug):
        project = get_object_or_404(
            Project, slug=project_slug, user=request.user
        )

        has_active_plan = project.live_plans.filter(
            expires_at__gte=timezone.now() - timedelta(days=GRACE_DAYS)
        ).exists()

        if not has_active_plan:
            return Response(
                {"error": "No active subscription found"},
                status=403
            )

        try:
            rename_live_tables_and_fields(
                project,
                table_renames=request.data.get("table_renames", {}),
                field_renames=request.data.get("field_renames", {}),
            )

            live_version = update_live_from_preview(project)

        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response({
            "message": "Live version updated successfully",
            "live_version_updated_at": live_version.updated_at
        })

    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from generate.models import Project, ProjectVersion, ExpiredProject
from .models import GRACE_DAYS, LiveUsagePlan
from django.utils import timezone
from datetime import timedelta

class ProjectExpireAPIView(APIView):
    """
    POST: Move live project version to expired snapshot if subscription is fully expired
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, project_slug):
        # 1️⃣ Get the project
        project = get_object_or_404(Project, slug=project_slug, user=request.user)

        # 2️⃣ Get latest live usage plan
        live_plan = project.live_plans.order_by("-expires_at").first()

        if not live_plan:
            # Treat as expired if no plan exists
            pass
        else:
            # 3️⃣ Check subscription status
            plan_status = live_plan.get_subscription_status()
            status = plan_status.get("status")

            # Don't expire if still active, expiring, or in grace period
            if status in ["active", "expiring", "grace"]:
                return Response(
                    {"message": f"Project is not expired yet, current status: '{status}'."}
                )

        # 4️⃣ Get live project version
        try:
            live_version = project.versions.get(version_type="live")
        except ProjectVersion.DoesNotExist:
            return Response({"message": "No live project version to expire."})

        # 5️⃣ Move live version to expired snapshot
        ExpiredProject.objects.create(
            project=project,
            ui_schema=live_version.ui_schema,
            workflows=live_version.workflows,
            data_types=live_version.data_types,
            live_app_data=live_version.app_data,
            expired_at=timezone.now(),
            grace_ended_at=timezone.now() + timedelta(days=GRACE_DAYS),
            reason="subscription_expired",
        )

        # 6️⃣ Delete live project version
        live_version.delete()

        return Response({"message": f"Live version of '{project_slug}' moved to expired snapshot."})




# payments/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from payments.models import Payment

class NEFTUploadView(APIView):
    """
    Upload NEFT screenshot for PLATFORM prompt packs
    """
    permission_classes = [IsAuthenticated]

    PLATFORM_PROMPT_PACKS = {
        "starter": {"credits": 5, "amount": 500},
        "pro": {"credits": 10, "amount": 1000},
    }

    def post(self, request):
        user = request.user
        pack = request.data.get("pack")
        screenshot = request.FILES.get("platform_neft_screenshot")

        if pack not in self.PLATFORM_PROMPT_PACKS:
            return Response(
                {"error": "Invalid prompt pack"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not screenshot:
            return Response(
                {"error": "NEFT screenshot is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pack_info = self.PLATFORM_PROMPT_PACKS[pack]

        payment = Payment.objects.create(
            paid_by=user,
            payment_for="platform",
            prompt_credits=pack_info["credits"],
            amount=pack_info["amount"],
            platform_neft_screenshot=screenshot,  # ✅ FIX
            razorpay_order_id=f"NEFT-PLATFORM-{user.id}-{Payment.objects.count()+1}",
            status="created",
        )

        return Response({
            "message": "NEFT submitted. Admin will credit prompts after verification.",
            "payment_id": payment.id,
            "credits": pack_info["credits"]
        }, status=status.HTTP_201_CREATED)
    

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from payments.models import Payment
from generate.models import Project

class LiveNEFTUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    LIVE_PLANS = {
        "1_month": 499,
        "6_months": 2799,
        "12_months": 4999,
    }

    def post(self, request, project_slug):
        user = request.user
        plan = request.data.get("plan")
        screenshot = request.FILES.get("screenshot")

        if plan not in self.LIVE_PLANS:
            return Response({"error": "Invalid plan"}, status=400)

        if not screenshot:
            return Response({"error": "Screenshot required"}, status=400)

        project = get_object_or_404(Project, slug=project_slug, user=user)

        payment = Payment.objects.create(
            paid_by=user,
            project=project,
            payment_for="live",
            plan=plan,
            amount=self.LIVE_PLANS[plan],
            live_neft_screenshot=screenshot,  # ✅ FIX
            razorpay_order_id=f"NEFT-LIVE-{user.id}-{Payment.objects.count()+1}",
            status="created",
        )

        return Response({
            "message": "NEFT submitted. Project will go live after verification.",
            "payment_id": payment.id
        }, status=201)