from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, ProjectVersion


# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email",
            "password", "first_name", "last_name"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ------------------------
# Project Serializer
# ------------------------
class ProjectSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "project_name", "description",
            "created_at", "updated_at", "user_name"
        ]

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


# ------------------------
# Project Version Serializer (Bubble-style)
# ------------------------
class ProjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = [
            "id",
            "version_type",      # preview / live
            "ui_schema",
            "workflows",
            "data_types",
            "app_data",
            "version_number",
            "updated_at",
        ]


# ------------------------
# Editor Load Serializer
# ------------------------
class ProjectDetailSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    project_name = serializers.CharField()
    version_type = serializers.CharField()

    ui_schema = serializers.JSONField()
    workflows = serializers.JSONField()
    data_types = serializers.JSONField()
    app_data = serializers.JSONField()
