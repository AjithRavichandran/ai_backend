# payment.models

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from generate.models import Project
from django.core.exceptions import ValidationError

# Create your models here.
class Payment(models.Model):

    PAYMENT_FOR_CHOICES = (
        ("live", "Live App Plan"),
        ("platform", "Platform Plan"),  # ✅ ADD THIS
    )


    plan = models.CharField(
        max_length=20,
        choices=[
            ('1_month', '1 Month'),
            ('6_months', '6 Months'),
            ('12_months', '12 Months'),
        ],
        null=True,
        blank=True
    )

    PLATFORM_PROMPT_PACKS = {
        "starter": {
            "credits": 5,
            "amount": 500,
        },
        "pro": {
            "credits": 10,
            "amount": 1000,
        },
    }

    # ✅ NEFT screenshots (separated clearly)
    live_neft_screenshot = models.ImageField(
        upload_to="neft/live/",
        null=True,
        blank=True,
        help_text="NEFT screenshot for Live project payment"
    )

    platform_neft_screenshot = models.ImageField(
        upload_to="neft/platform/",
        null=True,
        blank=True,
        help_text="NEFT screenshot for Platform credit payment"
    )


    prompt_credits = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Used only for platform payments"
    )


    # Who paid (for audit only)
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments_made"
    )

    # What is being paid for (MAIN OWNER)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,       
        blank=True   
    )

    payment_for = models.CharField(
        max_length=20,
        choices=PAYMENT_FOR_CHOICES,
        default="live"
    )

    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")

    status = models.CharField(
        max_length=20,
        choices=[
            ("created", "Created"),
            ("paid", "Paid"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
        default="created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # LIVE = project based + time plan
        if self.payment_for == "live":
            if not self.project:
                raise ValidationError("Live payments must be linked to a project")
            if not self.plan:
                raise ValidationError("Live payments must have a plan")
            if self.prompt_credits:
                raise ValidationError("Live payments cannot have prompt credits")

        # PLATFORM = user based + prompt packs
        if self.payment_for == "platform":
            if not self.paid_by:
                raise ValidationError("Platform payments must be linked to a user")

            if self.project:
                raise ValidationError("Platform payments must not be linked to a project")

            if self.prompt_credits is None or self.prompt_credits <= 0:
                raise ValidationError("Platform payments must include valid prompt credits")

            if self.plan:
                raise ValidationError("Platform payments must not have a plan")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        owner = self.project if self.project else self.paid_by
        return f"{owner} | {self.amount} | {self.status}"


class PlatformUsage(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="platform_usage"
    )

    # Free trial
    free_prompts_used = models.PositiveIntegerField(default=0)
    FREE_PROMPT_LIMIT = 2

    # Paid credits
    paid_prompt_credits = models.PositiveIntegerField(default=0)

    def can_use_prompt(self):
        return (
            self.free_prompts_used < self.FREE_PROMPT_LIMIT
            or self.paid_prompt_credits > 0
        )

    def consume_prompt(self):
        if self.free_prompts_used < self.FREE_PROMPT_LIMIT:
            self.free_prompts_used += 1
        elif self.paid_prompt_credits > 0:
            self.paid_prompt_credits -= 1
        else:
            raise ValidationError("No prompt credits left")

        self.save(update_fields=["free_prompts_used", "paid_prompt_credits"])


from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from generate.models import Project
from django.conf import settings
from django.utils.dateparse import parse_datetime
GRACE_DAYS = 5
EXPIRY_WARNING_DAYS = 5
import math

class LiveUsagePlan(models.Model):
    PLAN_CHOICES = [
        ("1_month", "1 Month"),
        ("6_months", "6 Months"),
        ("12_months", "12 Months"),
    ]

    project = models.ForeignKey(       # ✅ PROJECT
        Project,
        on_delete=models.CASCADE,
        related_name="live_plans"
    )

    payment = models.OneToOneField(    # ✅ PAYMENT RECORD
        Payment,
        on_delete=models.CASCADE,
        related_name="live_plan"
    )

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)


    reminder_sent_days_before = models.JSONField(default=list)
    grace_reminder_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # ensure started_at is datetime
            if isinstance(self.started_at, str):
                self.started_at = parse_datetime(self.started_at) or timezone.now()
            durations = {
                "1_month": 30,
                "6_months": 182,
                "12_months": 365,
            }
            self.expires_at = self.started_at + timedelta(days=durations[self.plan])
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() <= self.expires_at + timedelta(days=GRACE_DAYS)


    def get_subscription_status(self):
        now = timezone.now()
        expiry = self.expires_at
        grace_end = expiry + timedelta(days=GRACE_DAYS)

        if not expiry:
            return {
                "status": "expired",
                "days_left": 0,
                "message": None,
            }

        if now <= expiry:
            days_left = max(
                1,
                math.ceil((expiry - now).total_seconds() / 86400)
            )

            if days_left <= EXPIRY_WARNING_DAYS:
                return {
                    "status": "expiring",
                    "days_left": days_left,
                    "message": None,
                }

            return {
                "status": "active",
                "days_left": days_left,
                "message": None,
            }

        if expiry < now <= grace_end:
            days_left = max(
                1,
                math.ceil((grace_end - now).total_seconds() / 86400)
            )

            return {
                "status": "grace",
                "days_left": days_left,
                "message": None,
            }

        return {
            "status": "expired",
            "days_left": 0,
            "message": None,
        }


