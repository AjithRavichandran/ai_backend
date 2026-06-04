from django.contrib import admin
from django.utils.html import format_html
from django.db import transaction
from django.utils import timezone

from payments.models import Payment, PlatformUsage, LiveUsagePlan
from payments.views import first_time_or_after_expiry_promote_preview_to_live
from django.core.mail import send_mail
from django.conf import settings

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # ============================================================
    # LIST VIEW
    # ============================================================
    list_display = (
        "id",
        "paid_by",
        "payment_for",
        "project",
        "plan",
        "prompt_credits",
        "amount",
        "status",
        "live_neft_preview",
        "platform_neft_preview",
        "created_at",
    )

    list_filter = (
        "payment_for",
        "status",
        "plan",
        "created_at",
    )

    search_fields = (
        "id",
        "paid_by__username",
        "project__project_name",
        "razorpay_order_id",
    )

    ordering = ("-created_at",)

    # ============================================================
    # READONLY FIELDS
    # ============================================================
    readonly_fields = (
        "created_at",
        "razorpay_order_id",
        "razorpay_payment_id",
        "razorpay_signature",
        "live_neft_preview",
        "platform_neft_preview",
    )

    # ============================================================
    # FORM LAYOUT
    # ============================================================
    fieldsets = (
        ("Payment Info", {
            "fields": ("payment_for", "status", "amount", "currency")
        }),

        ("Live App Details", {
            "fields": ("project", "plan", "live_neft_screenshot", "live_neft_preview"),
            "classes": ("collapse",),
        }),

        ("Platform Credits", {
            "fields": ("paid_by", "prompt_credits", "platform_neft_screenshot", "platform_neft_preview"),
            "classes": ("collapse",),
        }),

        ("Razorpay Details", {
            "fields": ("razorpay_order_id", "razorpay_payment_id", "razorpay_signature"),
            "classes": ("collapse",),
        }),

        ("Meta", {
            "fields": ("created_at",),
        }),
    )

    actions = ["approve_payments", "reject_payments"]

    # ============================================================
    # NEFT IMAGE PREVIEWS
    # ============================================================
    def live_neft_preview(self, obj):
        if obj.live_neft_screenshot:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:110px;border-radius:8px;box-shadow:0 0 8px rgba(0,0,0,.4)" />'
                '</a>',
                obj.live_neft_screenshot.url,
                obj.live_neft_screenshot.url,
            )
        return "—"
    live_neft_preview.short_description = "Live NEFT Screenshot"

    def platform_neft_preview(self, obj):
        if obj.platform_neft_screenshot:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:110px;border-radius:8px;box-shadow:0 0 8px rgba(0,0,0,.4)" />'
                '</a>',
                obj.platform_neft_screenshot.url,
                obj.platform_neft_screenshot.url,
            )
        return "—"
    platform_neft_preview.short_description = "Platform NEFT Screenshot"

    # ============================================================
    # ADMIN ACTIONS
    # ============================================================
    @admin.action(description="✅ Approve payment (safe)")
    def approve_payments(self, request, queryset):
        approved = 0

        with transaction.atomic():
            for payment in queryset.select_related("project", "paid_by"):
                if payment.status == "paid":
                    continue

                # ---------------- PLATFORM PAYMENT ----------------
                if payment.payment_for == "platform":
                    usage, _ = PlatformUsage.objects.get_or_create(user=payment.paid_by)
                    usage.paid_prompt_credits += payment.prompt_credits
                    usage.save(update_fields=["paid_prompt_credits"])

                    # ---------------- SEND EMAIL ----------------
                    try:
                        subject = "Platform Credits Added!"
                        message = (
                            f"Hi {payment.paid_by.username},\n\n"
                            f"Your payment for platform credits has been approved.\n"
                            f"{payment.prompt_credits} prompt credits have been added to your account.\n\n"
                            f"Thank you for choosing PCL Infotech!"
                        )
                        recipient_list = [payment.paid_by.email]
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                    except Exception as e:
                        self.message_user(
                            request,
                            f"⚠ Email failed for {payment.paid_by.email}: {str(e)}",
                            level="warning",
                        )

                # ---------------- LIVE PAYMENT ----------------
                elif payment.payment_for == "live":
                    project = payment.project

                    # Create LiveUsagePlan if missing
                    if not hasattr(payment, "live_plan"):
                        LiveUsagePlan.objects.create(
                            project=project,
                            payment=payment,
                            plan=payment.plan,
                            started_at=timezone.now(),
                        )

                    # Promote preview → live
                    first_time_or_after_expiry_promote_preview_to_live(project)

                    # ---------------- SEND EMAIL ----------------
                    try:
                        project_slug = project.slug

                        # Get live ProjectVersion
                        live_version = project.versions.filter(version_type="live").first()
                        page_slug = ""  # default empty if no visible page found

                        if live_version:
                            pages = live_version.ui_schema.get("pages", [])
                            for page in pages:
                                if not page.get("hidden", False):
                                    from django.utils.text import slugify
                                    page_slug = slugify(page.get("name", ""))
                                    break

                        # Construct live URL
                        if settings.DEBUG:
                            live_url = f"http://localhost:3000/{project_slug}/{page_slug}"
                        else:
                            live_url = f"https://{project_slug}.{settings.FRONTEND_URL}/{page_slug}"

                        subject = f"Your project '{project.project_name}' is now live!"
                        message = (
                            f"Hi {payment.paid_by.username},\n\n"
                            f"Your payment for the live project '{project.project_name}' has been approved.\n"
                            f"The project is now live and visible to everyone.\n"
                            f"Visit your project: {live_url}\n\n"
                            f"Thank you for choosing PCL Infotech!"
                        )
                        recipient_list = [payment.paid_by.email]
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

                    except Exception as e:
                        self.message_user(
                            request,
                            f"⚠ Email failed for {payment.paid_by.email}: {str(e)}",
                            level="warning",
                        )

                # Mark payment as paid
                payment.status = "paid"
                payment.save(update_fields=["status"])

                approved += 1

        self.message_user(request, f"✅ {approved} payment(s) approved successfully.")
    @admin.action(description="❌ Reject payment")
    def reject_payments(self, request, queryset):
        updated = queryset.exclude(status="paid").update(status="failed")
        self.message_user(request, f"❌ {updated} payment(s) rejected.")