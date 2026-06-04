# generate.models

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db import IntegrityError, transaction

# --------------------------------------------------
# PROJECT (container only)
# --------------------------------------------------
class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    project_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_opened_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (
            ("user", "project_name"),  # ✅ user cannot have same project twice
        )
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "updated_at"]),
            models.Index(fields=["user"]),  # slug already indexed via unique
        ]

    def __str__(self):
        return f"{self.project_name} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.project_name)
            for i in range(100):
                slug = f"{base_slug}-{i}" if i else base_slug
                self.slug = slug
                try:
                    with transaction.atomic():
                        return super().save(*args, **kwargs)
                except IntegrityError:
                    continue
            raise Exception("Unable to generate unique slug")
        super().save(*args, **kwargs)


    def mark_opened(self):
        self.last_opened_at = timezone.now()
        self.save(update_fields=["last_opened_at"])

from django.db.models import Max
# --------------------------------------------------
# PROJECT VERSION (preview / live)
# --------------------------------------------------
class ProjectVersion(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version_type = models.CharField(
        max_length=10,
        choices=[("preview", "Preview"), ("live", "Live")]
    )

    # Editor state
    ui_schema = models.JSONField(default=dict)
    workflows = models.JSONField(default=list)
    data_types = models.JSONField(default=dict)

    # Runtime DB snapshot
    app_data = models.JSONField(default=dict)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "version_type"],
                name="one_version_per_type_per_project"
            )
        ]

    def __str__(self):
        return f"{self.project.project_name} - {self.version_type}"


# --------------------------------------------------
# EXPIRED PROJECT SNAPSHOT
# --------------------------------------------------
class ExpiredProject(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="expired_snapshot"
    )

    # Versioned editor state
    ui_schema = models.JSONField(default=dict)
    workflows = models.JSONField(default=list)
    data_types = models.JSONField(default=dict)

    live_app_data = models.JSONField(default=dict)

    expired_at = models.DateTimeField(default=timezone.now)
    grace_ended_at = models.DateTimeField()

    reason = models.CharField(
        max_length=50,
        default="subscription_expired"
    )

    def __str__(self):
        return f"Expired snapshot: {self.project.project_name}"

class BeforeDeployLiveAppData(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="live_data"
    )
    data = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Live data for {self.project.project_name}"


import uuid

class AppSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    user_id = models.CharField(max_length=64)  
    user_data = models.JSONField()              

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["expires_at"]),
            models.Index(fields=["project", "user_id"]),
        ]

    def is_valid(self):
        return self.expires_at > timezone.now()
    

