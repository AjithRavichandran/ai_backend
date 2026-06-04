from django.shortcuts import render
from django.utils import timezone
from generate.models import Project, ProjectVersion, AppSession
import uuid
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from generate.models import Project, AppSession
from datetime import timedelta


def get_session_ttl(version_type: str):
    if version_type == "preview":
        return timedelta(minutes=30)
    return timedelta(days=30)


class SecondaryUserSessionAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, project_slug):
        version_type = request.GET.get("version_type", "live")
        cookie_name = f"sessionId_{project_slug}_{version_type}"
        session_id = request.COOKIES.get(cookie_name)

        if not session_id:
            return Response({"user": None}, status=200)

        project = get_object_or_404(Project, slug=project_slug)

        session = AppSession.objects.filter(
            id=session_id,
            project=project,
            expires_at__gt=timezone.now()
        ).first()

        if not session:
            return Response({"user": None}, status=200)  # ✅ FIX

        return Response({"user": session.user_data}, status=200)

from django.contrib.auth.hashers import check_password

class SecondaryUserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, project_slug):
        project = get_object_or_404(Project, slug=project_slug)
        version_type = request.GET.get("version_type", "preview").lower()

        version = ProjectVersion.objects.filter(
            project=project,
            version_type=version_type
        ).first()

        if not version:
            return Response(
                {"status": "error", "message": "No project version found"},
                status=404
            )

        email = request.data.get("email")
        password = request.data.get("password")

        users = (version.app_data or {}).get("users", [])
        user = next((u for u in users if u.get("email") == email), None)

        if not user or not check_password(password, user.get("passwordHash")):
            return Response(
                {"status": "error", "message": "Invalid credentials"},
                status=401
            )

        # Invalidate old sessions
        AppSession.objects.filter(
            project=project,
            user_id=user["id"]
        ).delete()

        ttl = get_session_ttl(version_type)
        session_id = str(uuid.uuid4())

        AppSession.objects.create(
            id=session_id,
            project=project,
            user_id=user["id"],
            user_data=user,
            expires_at=timezone.now() + ttl
        )

        cookie_name = f"sessionId_{project.slug}_{version_type}"

        response = Response({
            "status": "success",
            "user": user,
            "sessionId": session_id,
        })

        response.set_cookie(
            cookie_name,
            session_id,
            max_age=int(ttl.total_seconds()),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        return response


class SecondaryUserUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, project_slug):
        version_type = request.GET.get("version_type", "preview").lower()
        cookie_name = f"sessionId_{project_slug}_{version_type}"

        session_id = request.COOKIES.get(cookie_name)
        if not session_id:
            return Response(
                {"status": "error", "message": "Not authenticated"},
                status=401
            )

        project = get_object_or_404(Project, slug=project_slug)

        session = AppSession.objects.filter(
            id=session_id,
            project=project,
            expires_at__gt=timezone.now()
        ).first()

        if not session:
            return Response(
                {"status": "error", "message": "Invalid session"},
                status=401
            )

        # ✅ Load correct version (preview or live)
        version = ProjectVersion.objects.filter(
            project=project,
            version_type=version_type
        ).first()

        if not version:
            return Response(
                {"status": "error", "message": "Project version not found"},
                status=404
            )

        app_data = version.app_data or {}
        users = app_data.get("users", [])

        user = next(
            (u for u in users if str(u.get("id")) == str(session.user_id)),
            None
        )

        if not user:
            return Response(
                {"status": "error", "message": "User not found"},
                status=404
            )

        allowed_fields = ["name", "email", "phone"]
        updated = False

        for field in allowed_fields:
            if field in request.data:
                user[field] = request.data[field]
                updated = True

        if not updated:
            return Response(
                {"status": "error", "message": "No valid fields"},
                status=400
            )

        # ✅ Save to ProjectVersion
        version.app_data = app_data
        version.save(update_fields=["app_data"])

        # ✅ Keep session snapshot in sync
        session.user_data = user
        session.save(update_fields=["user_data"])

        return Response({"status": "success", "user": user})
    
class CreateThingAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, project_slug, thing_type):
        version_type = request.GET.get("version_type", "live").lower()
        project = get_object_or_404(Project, slug=project_slug)

        version = ProjectVersion.objects.filter(
            project=project,
            version_type=version_type
        ).first()

        if not version:
            return Response(
                {"status": "error", "message": f"No {version_type} version found"},
                status=404
            )

        app_data = version.app_data or {}
        things = app_data.get(thing_type, [])

        # Generate ID
        # ----------------------------
        # Generate SAFE numeric ID
        # ----------------------------
        existing_ids = []

        for t in things:
            try:
                existing_ids.append(int(t.get("id", 0)))
            except (TypeError, ValueError):
                pass  # ignore bad ids safely

        new_id = max(existing_ids + [0]) + 1
        new_thing = {"id": new_id}


        # ------------------------------------
        # STEP 1: collect existing field names
        # ------------------------------------
        existing_keys = set()
        for item in things:
            existing_keys.update(item.keys())

        # ------------------------------------
        # STEP 2: copy request data AS-IS
        # ------------------------------------
        if isinstance(request.data, dict):
            if "fieldsMap" in request.data:
                for k, v in request.data["fieldsMap"].items():
                    if isinstance(v, dict) and "value" in v:
                        new_thing[k] = v["value"]
            else:
                for k, v in request.data.items():
                    new_thing[k] = v

        # ------------------------------------
        # STEP 3: fill missing existing fields
        # ------------------------------------
        for key in existing_keys:
            if key not in new_thing:
                new_thing[key] = None

        # Save
        things.append(new_thing)
        app_data[thing_type] = things
        version.app_data = app_data
        version.save(update_fields=["app_data"])

        return Response(
            {"status": "success", "data": new_thing},
            status=201
        )


class SecondaryUserCredentialsUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, project_slug):
        version_type = request.query_params.get("version_type", "preview").lower()
        project = get_object_or_404(Project, slug=project_slug)

        cookie_name = f"sessionId_{project_slug}_{version_type}"
        session_id = request.COOKIES.get(cookie_name)

        if not session_id:
            return Response({"status": "error", "message": "Not authenticated"}, status=401)

        session = AppSession.objects.filter(
            id=session_id,
            project=project,
            expires_at__gt=timezone.now()
        ).first()

        if not session:
            return Response({"status": "error", "message": "Invalid session"}, status=401)

        version = ProjectVersion.objects.filter(
            project=project,
            version_type=version_type
        ).first()

        if not version:
            return Response({"status": "error", "message": "Project version not found"}, status=404)

        app_data = version.app_data or {}
        users = app_data.get("users", [])

        user = next(
            (u for u in users if str(u.get("id")) == str(session.user_id)),
            None
        )

        if not user:
            return Response({"status": "error", "message": "User not found"}, status=404)

        email = request.data.get("email")
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("password")
        confirm_password = request.data.get("confirmPassword")

        if new_password:
            if not old_password:
                return Response({"status": "error", "message": "Old password required"}, status=400)

            if not check_password(old_password, user.get("passwordHash", "")):
                return Response({"status": "error", "message": "Wrong password"}, status=400)

            if new_password != confirm_password:
                return Response({"status": "error", "message": "Passwords do not match"}, status=400)

            user["passwordHash"] = make_password(new_password)

        if email:
            user["email"] = email

        version.app_data = app_data
        version.save(update_fields=["app_data"])

        session.user_data = user
        session.save(update_fields=["user_data"])

        return Response({"status": "success", "user": user})

from django.db import transaction
from django.contrib.auth.hashers import make_password
import copy
def is_image(value):
    if not isinstance(value, str):
        return False

    image_ext = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    return value.lower().startswith(("http://", "https://", "/media/")) \
           and value.lower().endswith(image_ext)


def is_empty(value):
    return value in ("", None, [], {}, "null", "none", 0)


def fill_missing_fields(user, defaults):
    result = copy.deepcopy(defaults)

    for key, default_value in defaults.items():
        user_value = user.get(key)

        # ⭐ IMAGE RULE — keep valid image URLs
        if is_image(user_value):
            result[key] = user_value
            continue

        # fallback logic
        if key not in user or is_empty(user_value):
            result[key] = copy.deepcopy(default_value)
        else:
            if isinstance(user_value, dict) and isinstance(default_value, dict):
                result[key] = fill_missing_fields(user_value, default_value)
            else:
                result[key] = user_value

    # preserve extra user fields
    for key, value in user.items():
        if key not in result:
            result[key] = value

    return result
def default_for_type(field_type, cardinality="single"):
    base = {
        "text": "",
        "email": "",
        "number": 0,
        "boolean": False,
        "date": timezone.now().date().isoformat(),
        "image": "",   # ← profilepic default
    }

    value = base.get(field_type, None)

    if cardinality == "list":
        return []

    return value

def build_user_schema_defaults(version):
    data_types = version.data_types or []

    # normalize structure
    if isinstance(data_types, dict):
        data_types = list(data_types.values())

    for dt in data_types:
        if dt.get("name") == "users":
            defaults = {}

            for field in dt.get("fields", []):
                fname = field.get("name")
                ftype = field.get("type")
                card = field.get("cardinality", "single")

                defaults[fname] = default_for_type(ftype, card)

            return defaults

    print("⚠ USERS SCHEMA NOT FOUND")
    return {}

class SecondaryUserSignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, project_slug):
        project = get_object_or_404(Project, slug=project_slug)

        # ---------------------------------
        # Version (default = preview)
        # ---------------------------------
        version_type = request.GET.get("version_type", "preview").lower()

        version = ProjectVersion.objects.filter(
            project=project,
            version_type=version_type
        ).first()

        if not version:
            return Response(
                {"status": "error", "message": "No project version found"},
                status=404
            )

        # ---------------------------------
        # Input validation
        # ---------------------------------
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name", "")

        if not email or not password:
            return Response(
                {"status": "error", "message": "Email & password required"},
                status=400
            )

        # ---------------------------------
        # Atomic user creation
        # ---------------------------------
        def safe_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        with transaction.atomic():
            version = ProjectVersion.objects.select_for_update().get(id=version.id)
            app_data = version.app_data or {}
            users = app_data.get("users", [])

            if any(u.get("email") == email for u in users):
                return Response(
                    {"status": "error", "message": "User already exists"},
                    status=409
                )

            next_user_id = max(
                [safe_int(u.get("id")) for u in users],
                default=0
            ) + 1

            next_platform_id = max(
                [safe_int(u.get("platformUserId")) for u in users],
                default=0
            ) + 1

            schema_defaults = build_user_schema_defaults(version)
            defaults = {**schema_defaults, **app_data.get("userDefaults", {})}

            # Create user
            new_user = {
                "id": next_user_id,
                "name": name or email.split("@")[0],
                "email": email,
                "passwordHash": make_password(password),  # ✅ SECURE
                "isAdmin": False,
                "createdAt": timezone.now().date().isoformat(),
                "platformUserId": next_platform_id,
            }

            new_user = fill_missing_fields(new_user, defaults)

            users.append(new_user)
            app_data["users"] = users

            version.app_data = app_data
            version.save(update_fields=["app_data"])

        # ---------------------------------
        # Session creation
        # ---------------------------------
        ttl = get_session_ttl(version_type)
        session_id = str(uuid.uuid4())
        safe_user = {k: v for k, v in new_user.items() if k != "passwordHash"}

        print("SAFE USER →", safe_user)

        AppSession.objects.create(
            id=session_id,
            project=project,
            user_id=safe_user["id"],
            user_data=safe_user,
            expires_at=timezone.now() + ttl
        )

        # ---------------------------------
        # Cookie
        # ---------------------------------
        cookie_name = f"sessionId_{project.slug}_{version_type}"

        response = Response({
            "status": "success",
            "user": safe_user,
            "sessionId": session_id,
        })

        response.set_cookie(
            cookie_name,
            session_id,
            max_age=int(ttl.total_seconds()),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        return response

 
import uuid
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from generate.models import Project, AppSession
class SecondaryUserLogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, project_slug):
        version_type = request.GET.get("version_type", "live").lower()
        cookie_name = f"sessionId_{project_slug}_{version_type}"

        project = get_object_or_404(Project, slug=project_slug)
        session_id = request.COOKIES.get(cookie_name)

        if session_id:
            try:
                session_uuid = uuid.UUID(session_id)
                AppSession.objects.filter(
                    id=session_uuid,
                    project=project
                ).delete()
            except (ValueError, TypeError):
                pass

        response = Response(
            {
                "status": "success",
                "message": "Logged out successfully",
            },
            status=200
        )

        # ✅ delete cookie (ONLY supported args)
        response.delete_cookie(
            cookie_name,
            path="/"
        )

        return response


from django.utils import timezone


