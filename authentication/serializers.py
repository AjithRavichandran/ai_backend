from rest_framework import serializers
from django.contrib.auth.models import User
from payments.models import LiveUsagePlan

class LiveUsagePlanSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    subscription_status = serializers.SerializerMethodField()
    project_slug = serializers.CharField(source="project.slug")
    project_name = serializers.CharField(source="project.project_name")

    class Meta:
        model = LiveUsagePlan
        fields = [
            "id",
            "plan",
            "started_at",
            "expires_at",
            "is_active",
            "subscription_status",
            "project_slug",
            "project_name",
        ]

    def get_is_active(self, obj):
        return obj.is_valid()

    def get_subscription_status(self, obj):
        return obj.get_subscription_status()


class UserSerializer(serializers.ModelSerializer):
    liveusageplan = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_superuser", "liveusageplan"]  # add is_superuser

    def get_liveusageplan(self, obj):
        project_slug = self.context.get("project_slug")

        if not project_slug:
            return None

        plan = (
            LiveUsagePlan.objects
            .filter(
                project__user=obj,
                project__slug=project_slug
            )
            .order_by("-started_at")
            .first()
        )

        if not plan:
            return None

        return LiveUsagePlanSerializer(plan).data
