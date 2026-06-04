# payments/management/commands/send_expiry_emails.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from payments.models import LiveUsagePlan, GRACE_DAYS
from django.conf import settings
from datetime import timedelta
import math

EXPIRY_WARNING_DAYS = 3  # warning before expiry

class Command(BaseCommand):
    help = "Send subscription expiry reminders to project owners"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        plans = LiveUsagePlan.objects.all()

        for plan in plans:
            if not plan.expires_at or not plan.project or not plan.project.user.email:
                continue

            user_email = plan.project.user.email

            # 1️⃣ Calculate days to expiry
            days_to_expiry = math.ceil((plan.expires_at - now).total_seconds() / 86400)

            # 2️⃣ Calculate remaining days in grace period
            grace_end = plan.expires_at + timedelta(days=GRACE_DAYS)
            days_in_grace = math.ceil((grace_end - now).total_seconds() / 86400)

            # Ensure list fields are initialized
            if plan.reminder_sent_days_before is None:
                plan.reminder_sent_days_before = []
            if plan.grace_reminder_sent_days is None:
                plan.grace_reminder_sent_days = []

            # 3️⃣ Pre-expiry reminders (3,2,1 days)
            if 0 < days_to_expiry <= EXPIRY_WARNING_DAYS:
                if days_to_expiry not in plan.reminder_sent_days_before:
                    send_mail(
                        subject=f"Your subscription expires in {days_to_expiry} day(s)",
                        message=(
                            f"Hello, your subscription for project '{plan.project.project_name}' "
                            f"expires in {days_to_expiry} day(s). Please renew to avoid interruption."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user_email],
                    )
                    plan.reminder_sent_days_before.append(days_to_expiry)
                    plan.save(update_fields=["reminder_sent_days_before"])

            # 4️⃣ Grace period reminders (5,4,3,2,1 days left)
            elif 0 < days_in_grace <= GRACE_DAYS:
                if days_in_grace not in plan.grace_reminder_sent_days:
                    send_mail(
                        subject=f"Your subscription expired, {days_in_grace} day(s) left in grace period",
                        message=(
                            f"Hello, your subscription for project '{plan.project.project_name}' has expired, "
                            f"but you have {days_in_grace} day(s) remaining in your grace period. "
                            "Please renew to continue using your project."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user_email],
                    )
                    plan.grace_reminder_sent_days.append(days_in_grace)
                    plan.save(update_fields=["grace_reminder_sent_days"])