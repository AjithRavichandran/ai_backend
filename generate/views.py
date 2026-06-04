import os, json, re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings
from pydantic import ValidationError
import pprint
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, ProjectDetailSerializer


# ✅ 1️⃣ List all projects for the logged-in user
class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return Response(
                {"detail": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_name = request.data.get("project_name")
        if not new_name:
            return Response(
                {"detail": "project_name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for uniqueness per user
        if Project.objects.filter(user=request.user, project_name=new_name).exclude(id=project_id).exists():
            return Response(
                {"detail": "Project name already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.project_name = new_name
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

def create_live_appdata_with_fields(app_datas):
    """
    Creates a safe live app data object that preserves all field names.
    Each table gets a single empty record to display headers in the frontend.
    """
    live_data = {}

    for table, records in app_datas.items():
        if records:
            # Take keys from the first record
            keys = records[0].keys()
        else:
            keys = []  # fallback if table has no records

        # Create a single empty record with all keys
        empty_record = {key: "" for key in keys}
        live_data[table] = [empty_record] if keys else []

    return live_data

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, ProjectVersion

class ProjectDetailCanvasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_slug):
        project = get_object_or_404(Project, slug=project_slug, user=request.user)

        # 1️⃣ Preview version (editor structure)
        version = ProjectVersion.objects.filter(
            project=project,
            version_type="preview"
        ).first()

        if not version:
            version = ProjectVersion.objects.create(
                project=project,
                version_type="preview",
                ui_schema={},
                workflows=[],
                data_types={},
                app_data={}
            )

        # 2️⃣ Decide source of LIVE app data
        live_version = ProjectVersion.objects.filter(
            project=project,
            version_type="live"
        ).first()

        if live_version:
            # 🟢 DEPLOYED → read from live ProjectVersion
            live_app_data = live_version.app_data

        else:
            # 🔵 NOT DEPLOYED → read from BeforeDeployLiveAppData
            live_data_obj = BeforeDeployLiveAppData.objects.filter(
                project=project
            ).first()

            if not live_data_obj:
                live_data_obj = BeforeDeployLiveAppData.objects.create(
                    project=project,
                    data=create_live_appdata_with_fields(version.app_data)
                )

            live_app_data = live_data_obj.data

        data = {
            "id": project.id,
            "project_name": project.project_name,

            # Preview
            "schema": version.ui_schema,
            "workflows": version.workflows,
            "datatypes": version.data_types,
            "appdata": version.app_data,

            # Live (dynamic source)
            "liveappdata": live_app_data,

            "version_type": version.version_type,
        }

        project.mark_opened()
        return Response(data)


import random

def apply_modifier(filtered, modifier):
    if not filtered:
        return []

    # Handle simple modifiers
    if modifier in ["first", "first-item"]:
        return filtered[:1]
    if modifier in ["last", "last-item"]:
        return filtered[-1:]
    if modifier in ["random", "random-item"]:
        return [random.choice(filtered)]

    # Handle each_item.<field>
    if modifier and modifier.startswith("each_item."):
        field = modifier.split(".", 1)[1]   # "name" or "price"
        return [r.get(field) for r in filtered if isinstance(r, dict)]

    return filtered
def resolve_do_search(search_expr, appdata, request, current_app_user):
    if not search_expr:
        return []

    search_type = search_expr.get("type")
    conditions = search_expr.get("conditions", [])
    modifier = search_expr.get("modifier")

    all_records = appdata.get(search_type, []) if appdata else []


    filtered = filter_json(
        records=all_records,
        conditions=conditions,
        request=request,
        current_app_user=current_app_user,
        modifier=None,
        appdata=appdata
    )

    # ✅ Apply modifier using helper
    return apply_modifier(filtered, modifier)



from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from generate.models import AppSession



def filter_json(records, conditions=None, request=None, current_app_user=None, modifier=None, appdata=None):
    conditions = conditions or []

    filtered = []


    def resolve_right_value(right, record, request, current_app_user, appdata=None):

        source = right.get("source")

        if source == "static":
            return right.get("value")

        if source == "request" and request:
            # e.g., ?filter_name=value
            return request.GET.get(right.get("value"))

        if source == "record":
            return record.get(right.get("field"))

        if source == "current_user":
            if not current_app_user:
                return None
            field = right.get("field")
            return current_app_user.get(field) if field else current_app_user.get("id")

        if source == "page_element" and request:
            # Any input element on page
            field_id = right.get("field")
            return request.GET.get(f"input_{field_id}")

        if source == "do_search":
            search_expr = right.get("search")
            result = resolve_do_search(
                search_expr,
                appdata,
                request,
                current_app_user
            )
            # Bubble: if list/dict, compare IDs
            if isinstance(result, dict):
                return result.get("id")
            return result

        # Future sources: you can add more here (e.g., session, workflow output)
        return None


      

    filtered = []

    for record in records:
        match = True

        for cond in conditions:
            operator = cond.get("operator")
            left_field = cond.get("left", {}).get("field")
            right = cond.get("right", {})

            # Ignore incomplete conditions
            if not left_field or not operator or not right.get("source"):
                continue

            left_value = record.get(left_field)
            right_value = resolve_right_value(right, record, request, current_app_user, appdata)

            # Normalize strings
            if isinstance(left_value, str):
                left_value = left_value.strip()
            if isinstance(right_value, str):
                right_value = right_value.strip()

            # Numeric coercion
            for side in ("left", "right"):
                val = left_value if side == "left" else right_value
                if isinstance(val, str):
                    try:
                        val = float(val) if "." in val else int(val)
                        if side == "left":
                            left_value = val
                        else:
                            right_value = val
                    except ValueError:
                        pass

            # =======================
            # ✅ Handle all operators
            # =======================
            if operator in ["=", "equals"]:
                if right_value in [None, ""]:  # skip empty input
                    continue
                if left_value != right_value:
                    match = False
                    break

            elif operator in ["!=", "not_equals"]:
                if right_value in [None, ""]:  # skip empty input
                    continue
                if left_value == right_value:
                    match = False
                    break

            elif operator == "contains":
                if right_value in [None, ""]:  # skip empty input
                    continue
                if left_value is None or str(right_value).lower() not in str(left_value).lower():
                    match = False
                    break

            elif operator == "startsWith":
                if right_value in [None, ""]:  # skip empty input
                    continue
                if left_value is None or not str(left_value).lower().startswith(str(right_value).lower()):
                    match = False
                    break

            elif operator == "endsWith":
                if right_value in [None, ""]:  # skip empty input
                    continue
                if left_value is None or not str(left_value).lower().endswith(str(right_value).lower()):
                    match = False
                    break

        if match:
            filtered.append(record)


    # 🔹 Apply modifier here (list datasource only)
    if modifier:
        if modifier in ["first", "first-item"]:
            return filtered[:1]
        if modifier in ["last", "last-item"]:
            return filtered[-1:]
        if modifier in ["random", "random-item"]:
            import random
            return [random.choice(filtered)] if filtered else []

    return filtered
import math

def apply_math_operator(left, operator, right=None):
    try:
        left = float(left)
        if right is not None:
            right = float(right)
    except (TypeError, ValueError):
        return None

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return left / right if right != 0 else None

    if operator == "round":
        return round(left)
    if operator == "floor":
        return math.floor(left)
    if operator == "ceil":
        return math.ceil(left)

    return None

def resolve_dynamic_expression(expr, appdata, request, current_app_user, popup=None, context_value=None):
    expr = expr.replace("each item's ", "*.")
    tokens = expr.split(".")
    i = 0
    value = context_value

    while i < len(tokens):
        token = tokens[i]

        # 🔥 NORMALIZE "each item's"
        if token in ["each item's", "each_item's", "each-item's", "each_item", "each-item"]:
            token = "*"

        # ----------------------------
        # search_for.<type>
        # ----------------------------
        if token == "search_for":
            search_type = tokens[i + 1]
            conditions = popup.get("conditions", []) if popup else []

            all_records = appdata.get(search_type, []) if appdata else []


            value = filter_json(
                records=all_records,
                conditions=conditions,
                request=request,
                current_app_user=current_app_user,
                modifier=None,
                appdata=appdata
            )
            i += 2
            continue

        # ----------------------------
        # modifiers
        # ----------------------------
        if token in ["first-item", "last-item", "random-item"]:
            if not isinstance(value, list) or not value:
                return None

            if token == "first-item":
                value = value[0]
            elif token == "last-item":
                value = value[-1]
            else:
                import random
                value = random.choice(value)

            i += 1
            continue

        # ----------------------------
        # star (*) → list spread OR multiply
        # ----------------------------
        # ----------------------------
# star (*) → list spread OR multiply
# ----------------------------
        # ----------------------------
# star (*) → list spread OR multiply
# ----------------------------
        if token == "*":

            # LIST SPREAD (each item's)
            if isinstance(value, list):
                field = tokens[i + 1]   # 👈 name / price / etc
                results = []

                for item in value:
                    if isinstance(item, dict):
                        results.append(item.get(field))
                    else:
                        results.append(None)

                value = results
                i += 2      # 👈 VERY IMPORTANT (skip * and field)
                continue

            # MULTIPLY (math *)
            right_expr = ".".join(tokens[i + 1:])
            right_value = resolve_dynamic_expression(
                right_expr,
                appdata,
                request,
                current_app_user,
                popup=popup
            )

            return apply_math_operator(value, "*", right_value)

        # ----------------------------
# list aggregations: sum, count, average
# ----------------------------
        # ----------------------------
        # aggregations
        # ----------------------------
        if token in ["sum", "count", "average", "min", "max", "median", "product"]:
          if not isinstance(value, list):
              return None

          # ✅ Convert to numbers safely
          nums = [
              float(v)
              for v in value
              if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit()
          ]

          if token == "count":
              value = len(nums)
          elif token == "sum":
              value = round(sum(nums), 2)
          elif token == "average":
              value = round(sum(nums) / len(nums), 2) if nums else None
          elif token == "min":
              value = round(min(nums), 2) if nums else None
          elif token == "max":
              value = round(max(nums), 2) if nums else None
          elif token == "median":
              if not nums:
                  value = None
              else:
                  nums.sort()
                  n = len(nums)
                  mid = n // 2
                  if n % 2 == 0:
                      value = round((nums[mid - 1] + nums[mid]) / 2, 2)
                  else:
                      value = round(nums[mid], 2)
          elif token == "product":
              from functools import reduce
              import operator
              value = round(reduce(operator.mul, nums, 1), 2) if nums else None

          i += 1
          continue



        # ----------------------------
        # arithmetic + - /
        # ----------------------------
        if token in ["+", "-", "/"]:
            right_expr = ".".join(tokens[i + 1:])
            right_value = resolve_dynamic_expression(
                right_expr,
                appdata,
                request,
                current_app_user,
                popup=popup
            )

            return apply_math_operator(value, token, right_value)

        # ----------------------------
        # math functions
        # ----------------------------
        if token in ["round", "floor", "ceil"]:
            return apply_math_operator(value, token)

        # ----------------------------
        # field access
        # ----------------------------
        if isinstance(value, dict):
            value = value.get(token)
            i += 1
            continue

        return None

    return value


def resolve_dynamic_data(element, appdata, request=None, current_app_user=None):
    expr = element.get("dynamicData")
    popup = element.get("dynamicDataPopup") or {}

    if not expr:
        return None

    # Bubble behavior
    if expr.startswith("current_user") and not current_app_user:
        return None

    return resolve_dynamic_expression(
        expr=expr,
        appdata=appdata,
        request=request,
        current_app_user=current_app_user,
        popup=popup,
        context_value=None
    )

def resolve_conditional(conditional, current_app_user):
    if not conditional:
        return True  # no condition = show element

    source = conditional.get("source")
    operator = conditional.get("operator")

    if source == "current_user" and operator == "logged_in":
        return bool(current_app_user)

    if source == "current_user" and operator == "logged_out":
        return not bool(current_app_user)

    return True


def collect_dynamic_and_db(elements, appdata, request, db_list_data, dynamic_value, current_app_user=None, visited=None):
    if visited is None:
        visited = set()

    for el in elements:
        el_id = str(el["id"])

        if el_id in visited:
            continue
        visited.add(el_id)

        # Skip if conditional fails
        if not resolve_conditional(el.get("conditional"), current_app_user):
            continue

        # ------------------
        # Dynamic data (for individual elements)
        # ------------------
        if el.get("dynamicData"):
            dynamic_value[el_id] = resolve_dynamic_data(el, appdata, request, current_app_user)

        # ------------------
        # Repeating groups / data sources
        # ------------------
        if el.get("typeOfContent") and el.get("dataSource"):
            ds = el.get("dataSource")

            # Only fetch if dataSource has keys
            if ds and any(ds.values()):
                all_records = appdata.get(el["typeOfContent"], []) if appdata else []

                filtered = filter_json(
                    records=all_records,
                    conditions=ds.get("conditions", []),
                    request=request,
                    current_app_user=current_app_user,
                    modifier=ds.get("modifier"),
                    appdata=appdata
                )
                db_list_data[el_id] = filtered

                # If repeating group, also populate dynamic_value for its children
                if el.get("type") == "repeating_group" and el.get("children"):
                    rg_items = []
                    for item in filtered:
                        child_values = {}
                        for child in el["children"]:
                            child_copy = child.copy()
                            child_copy["parent_group"] = item
                            if child_copy.get("dynamicData"):
                                child_values[str(child_copy["id"])] = resolve_dynamic_data(
                                    child_copy, appdata, request, current_app_user
                                )
                        rg_items.append({
                            "parent_group": item,
                            "children": child_values
                        })
                    dynamic_value[el_id] = rg_items

        # ------------------
        # Recurse children
        # ------------------
        if el.get("children"):
            collect_dynamic_and_db(
                el["children"], appdata, request, db_list_data, dynamic_value,
                current_app_user, visited
            )


from rest_framework.permissions import BasePermission
import uuid
from django.utils import timezone
from generate.models import AppSession

def get_current_app_user(request, project, version_type="live"):
    if not request or not project:
        return None

    cookie_name = f"sessionId_{project.slug}_{version_type}"
    session_id = request.COOKIES.get(cookie_name)

    if not session_id:
        return None

    try:
        session_uuid = uuid.UUID(session_id)
    except (ValueError, TypeError):
        return None

    session = AppSession.objects.filter(
        id=session_uuid,
        project=project,
        expires_at__gt=timezone.now()
    ).first()

    if not session:
        return None

    session_user = session.user_data or {}
    user_id = session_user.get("id")

    if not user_id:
        return session_user

    # ✅ fetch fresh user from runtime app DB
    version = ProjectVersion.objects.filter(
        project=project,
        version_type=version_type
    ).first()

    if not version:
        return session_user

    app_users = version.app_data.get("users", [])

    fresh_user = next(
        (u for u in app_users if u.get("id") == user_id),
        None
    )

    return fresh_user or session_user


from django.core.exceptions import ObjectDoesNotExist

class AllowPreviewSession(BasePermission):
    def has_permission(self, request, view):
        # Always allow platform users
        if request.user and request.user.is_authenticated:
            return True
        
        # Always allow preview access for end users, even without a cookie
        return True


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

from .models import Project, ProjectVersion

from django.conf import settings

def inject_media_urls(node, request):
    """
    Walk schema recursively and replace image src
    with full media URL.
    """

    if isinstance(node, dict):

        if node.get("type") == "image" and "src" in node:
            src = node["src"]

            # avoid double injection
            if src and not src.startswith("http"):
                node["src"] = request.build_absolute_uri(
                    settings.MEDIA_URL + src
                )

        for value in node.values():
            inject_media_urls(value, request)

    elif isinstance(node, list):
        for item in node:
            inject_media_urls(item, request)

    return node

class ProjectDetailPreviewView(APIView):
    permission_classes = [AllowPreviewSession]

    def get(self, request, project_slug):
        # ---------------- Resolve project ----------------
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            raise NotFound("Project not found")

        # ---------------- Resolve app user ----------------
        current_app_user = get_current_app_user(request, project, version_type="preview")
        print("🍪 ALL COOKIES:", request.COOKIES)
        print("🟡 PREVIEW current_app_user:", current_app_user)

        # ---------------- Load PREVIEW version ONLY ----------------
        version = ProjectVersion.objects.filter(
            project=project,
            version_type="preview"
        ).first()

        if not version:
            raise NotFound("No preview version available")


        if not version:
            raise NotFound("No runtime version available")

        schema = version.ui_schema or {}
        schema = inject_media_urls(schema, request)  # <-- ADD THIS LINE

        workflow_data = version.workflows or []
        datatype_data = version.data_types or []
        appdata_data = version.app_data or {}

        db_list_data = {}
        dynamic_value = {}

        pages = schema.get("pages", [])

        for page in pages:
            if page.get("children"):
                collect_dynamic_and_db(
                    page["children"],
                    appdata_data,
                    request,
                    db_list_data,
                    dynamic_value,
                    current_app_user=current_app_user
                )
        print("dynamic value -")
        pprint.pprint(dynamic_value)

        # 🔒 RESPONSE KEYS UNCHANGED
        data = {
            "id": project.id,
            "project_name": project.project_name,
            "schema": schema,
            "workflows": workflow_data,
            "datatypes": datatype_data,
            "appdata": appdata_data,
            "db_list_data": db_list_data,
            "dynamic_value": dynamic_value,
            "loggedInUser": current_app_user,
        }

        return Response(data)


from rest_framework.permissions import AllowAny

class LiveProjectAPIView(APIView):
    permission_classes = [AllowAny]  # public live site

    def get(self, request, project_slug):
        project = get_object_or_404(Project, slug=project_slug)

        current_app_user = get_current_app_user(request, project, version_type="live")
        print("🍪 ALL COOKIES:", request.COOKIES)
        print("🟢 LIVE current_app_user:", current_app_user)
        
        version = ProjectVersion.objects.filter(
            project=project,
            version_type="live"
        ).first()

        active_plan = (
            project.live_plans
            .filter(expires_at__gt=timezone.now())
            .order_by("-expires_at")
            .first()
        )
        if not version or not active_plan:
            if not project.live_plans.exists():
                reason = "no_subscription"
                message = "Project has no active subscription"
            elif not active_plan:
                reason = "subscription_expired"
                message = "Subscription expired"
            else:
                reason = "not_deployed"
                message = "No live version deployed yet"

            return Response(
                {
                    "error": message,
                    "reason": reason,
                },
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        schema = version.ui_schema or {}
        schema = inject_media_urls(schema, request)
        workflow_data = version.workflows or []
        datatype_data = version.data_types or {}
        appdata_data = version.app_data or {}

        db_list_data = {}
        dynamic_value = {}

        pages = schema.get("pages", [])

        for page in pages:
            if page.get("children"):
                collect_dynamic_and_db(
                    page["children"],
                    appdata_data,
                    request,
                    db_list_data,
                    dynamic_value,
                    current_app_user=current_app_user
                )

        print("LIVE dynamic value -")
        pprint.pprint(dynamic_value)

        print("LIVE db_list data -")
        pprint.pprint(db_list_data)

        data = {
            "id": project.id,
            "project_name": project.project_name,
            "project_slug": project.slug,

            "schema": schema,
            "workflows": workflow_data,
            "datatypes": datatype_data,
            "appdata": appdata_data,

            "db_list_data": db_list_data,
            "dynamic_value": dynamic_value,

            "loggedInUser": current_app_user,
        }

        return Response(data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, ProjectVersion


class SaveAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        project = get_object_or_404(Project, pk=pk, user=user)

        schema_data = request.data.get("schema", {})
        workflow_wrapper = request.data.get("workflows", [])
        datatype_data = request.data.get("datatypes", [])
        appdata_data = request.data.get("appdata", {})

        # ---------------- Type safety ----------------
        schema_data = schema_data if isinstance(schema_data, dict) else {}
        datatype_data = datatype_data if isinstance(datatype_data, list) else []
        appdata_data = appdata_data if isinstance(appdata_data, dict) else {}

        # ---------------- Workflows normalization ----------------
        if isinstance(workflow_wrapper, list):
            workflow_data = workflow_wrapper
        elif isinstance(workflow_wrapper, dict):
            workflow_data = [workflow_wrapper]
        else:
            workflow_data = []

        # ---------------- Check for existing active preview ----------------
        preview = ProjectVersion.objects.filter(
            project=project,
            version_type="preview"
        ).first()


        if preview:
            preview.ui_schema = schema_data
            preview.workflows = workflow_data
            preview.data_types = datatype_data
            preview.app_data = appdata_data
            preview.save()
            message = "✅ Preview updated successfully"
        else:
            ProjectVersion.objects.create(
                project=project,
                version_type="preview",
                ui_schema=schema_data,
                workflows=workflow_data,
                data_types=datatype_data,
                app_data=appdata_data
            )
            message = "✅ Preview created successfully"

        return Response({
            "message": message,
            "version_type": "preview",
        }, status=200)



class SaveLiveAppDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """
        Save the live appdata for a project.
        """
        project = get_object_or_404(Project, id=project_id, user=request.user)
        live_data = request.data.get("liveappdata")

        if not isinstance(live_data, dict):
            return Response(
                {"error": "Invalid liveappdata format, must be a JSON object."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1️⃣ Check if LIVE ProjectVersion exists
        live_version = ProjectVersion.objects.filter(
            project=project,
            version_type="live"
        ).first()

        if live_version:
            # 🟢 Save ONLY in ProjectVersion
            live_version.app_data = live_data
            live_version.save(update_fields=["app_data", "updated_at"])

        else:
            # 🔵 OLD BEHAVIOR → save in BeforeDeployLiveAppData
            live_appdata_obj, _ = BeforeDeployLiveAppData.objects.get_or_create(
                project=project
            )
            live_appdata_obj.data = live_data
            live_appdata_obj.save()

        return Response(
            {"message": "Live AppData saved successfully."},
            status=status.HTTP_200_OK
        )

class PageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id, page_id):
        # Rename logic (copied from RenamePageAPIView)
        user = request.user
        project = get_object_or_404(Project, id=project_id, user=user)

        new_name = request.data.get("name", "").strip()
        if not new_name:
            return Response({"error": "Page name is required"}, status=400)

        version = ProjectVersion.objects.filter(project=project, version_type="preview").first()
        if not version:
            return Response({"error": "Preview version not found"}, status=404)

        schema = version.ui_schema or {}
        pages = schema.get("pages", [])

        for page in pages:
            if str(page.get("id")) == str(page_id):
                page["name"] = new_name
                break
        else:
            return Response({"error": "Page not found"}, status=404)

        version.ui_schema = schema
        version.save(update_fields=["ui_schema"])

        return Response({"success": True, "page": {"id": page_id, "name": new_name}}, status=200)

    def delete(self, request, project_id, page_id):
        # Delete logic (copied from ProjectPageDeleteView)
        project = get_object_or_404(Project, id=project_id, user=request.user)
        version = ProjectVersion.objects.filter(project=project, version_type="preview").first()
        if not version:
            return Response({"error": "Preview version not found"}, status=404)

        schema = version.ui_schema or {}
        pages = schema.get("pages", [])

        new_pages = [p for p in pages if str(p["id"]) != str(page_id)]
        if len(new_pages) == len(pages):
            return Response({"error": "Page not found"}, status=404)

        schema["pages"] = new_pages
        if schema.get("activePageId") == str(page_id):
            schema["activePageId"] = new_pages[0]["id"] if new_pages else None

        version.ui_schema = schema
        version.save(update_fields=["ui_schema"])

        return Response({"success": True}, status=200)


class ProjectPageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id, user=request.user)

        name = request.data.get("name", "").strip()
        if not name:
            return Response({"error": "Page name is required"}, status=400)

        version = ProjectVersion.objects.filter(project=project, version_type="preview").first()
        if not version:
            return Response({"error": "Preview version not found"}, status=404)

        schema = version.ui_schema or {}
        pages = schema.get("pages", [])

        # Find last numeric ID safely
        last_id = max([int(p["id"]) for p in pages if str(p["id"]).isdigit()] or [0])
        new_id = str(last_id + 1)

        new_page = {
            "id": new_id,
            "name": name,
            "width": 1500,
            "backgroundColor": "#ffffff",
            "children": [],
            "parentId": None,
            "indexInParent": len(pages),
            "type": "page",
        }

        pages.append(new_page)
        schema["pages"] = pages
        schema.setdefault("activePageId", new_id)


        version.ui_schema = schema
        version.save(update_fields=["ui_schema"])

        return Response({"success": True, "page": new_page, "version": "preview"}, status=201)

from .models import ExpiredProject

class RenameLiveTablesAndFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        # 1️⃣ Get the project
        project = get_object_or_404(Project, id=project_id)

        # 2️⃣ Get preview version (must exist)
        preview = get_object_or_404(
            ProjectVersion, project=project, version_type="preview"
        )

        # 3️⃣ Load live app_data with fallbacks and track source
        source = None
        live_appdata = {}

        try:
            live = ProjectVersion.objects.get(project=project, version_type="live")
            live_appdata = live.app_data or {}
            source = "live ProjectVersion"
        except ProjectVersion.DoesNotExist:
            live = None

        if not live_appdata:
            try:
                before_deploy = BeforeDeployLiveAppData.objects.get(project=project)
                live_appdata = before_deploy.data
                source = "BeforeDeployLiveAppData"
            except BeforeDeployLiveAppData.DoesNotExist:
                try:
                    expired_snapshot = ExpiredProject.objects.get(project=project)
                    live_appdata = expired_snapshot.live_app_data
                    source = "ExpiredProject snapshot"
                except ExpiredProject.DoesNotExist:
                    live_appdata = {}
                    source = "empty fallback"

        preview_appdata = preview.app_data or {}

        # 4️⃣ Get table and field rename mappings from request
        table_renames = request.data.get("table_renames", {})
        field_renames = request.data.get("field_renames", {})

        print("table_renames - ")
        pprint.pprint(table_renames)
        print("field_names - ")
        pprint.pprint(field_renames)
        print(f"💡 Live app_data source: {source}")

        # 5️⃣ Rename tables and fields
        renamed_live_appdata = {}
        for old_table, rows in live_appdata.items():
            new_table = table_renames.get(old_table, old_table)
            renamed_rows = []
            rename_fields_map = field_renames.get(old_table, {})

            for row in rows:
                new_row = {}
                for old_field, value in row.items():
                    new_field = rename_fields_map.get(old_field, old_field)
                    new_row[new_field] = value
                renamed_rows.append(new_row)

            renamed_live_appdata[new_table] = renamed_rows

        # 6️⃣ Sync with preview app_data
        final_live_appdata = {}
        for preview_table, preview_rows in preview_appdata.items():
            if preview_table not in renamed_live_appdata:
                if preview_rows:
                    empty_row = {k: "" for k in preview_rows[0].keys()}
                    final_live_appdata[preview_table] = [empty_row]
                else:
                    final_live_appdata[preview_table] = []
                continue

            live_rows = renamed_live_appdata[preview_table]
            final_rows = []

            preview_fields = set()
            for row in preview_rows:
                preview_fields.update(row.keys())

            for row in live_rows:
                filtered_row = {k: v for k, v in row.items() if k in preview_fields}
                final_rows.append(filtered_row)

            final_live_appdata[preview_table] = final_rows

        # 7️⃣ Save to the source it came from
        if source == "live ProjectVersion" and live:
            live.app_data = final_live_appdata
            live.save()
        elif source == "BeforeDeployLiveAppData":
            before_deploy.data = final_live_appdata
            before_deploy.save()
        elif source == "ExpiredProject snapshot":
            expired_snapshot.live_app_data = final_live_appdata
            expired_snapshot.save()
        else:
            # fallback (should not happen)
            if live:
                live.app_data = final_live_appdata
                live.save()

        # 8️⃣ Return response
        return Response(
            {
                "success": True,
                "final_live_appdata": final_live_appdata,
                "source": source
            },
            status=status.HTTP_200_OK
        )

import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.storage import default_storage
import uuid
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, element_id):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # ✅ Generate unique filename
        ext = file.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        # ✅ Save under `live/` folder
        file_path = f"live/{filename}"
        default_storage.save(file_path, file)

        # Return a URL that points to /media/live/...
        file_url = f"{settings.MEDIA_URL}{file_path}"  # /media/live/xxxx.jpg

        return JsonResponse({
            "success": True,
            "src": file_url,
            "filename": filename
        })


class reactjs(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        
        data = [
  { "id": 1, "name": "Virat", "img": "./assets/1.jpg", "rank": 1, "hidden": False },
  { "id": 2, "name": "MS Dhoni", "img": "./assets/2.jpg", "rank": 4, "hidden": False },
  { "id": 3, "name": "Rohit", "img": "./assets/3.jpg", "rank": 2, "hidden": False },
  { "id": 4, "name": "Hardik", "img": None, "rank": 3, "hidden": False }
]
        return Response({"data": data})



import traceback

from .models import BeforeDeployLiveAppData
from generate.navbar_helpers import add_navbar_buttons
from generate.globalPopups import globalPopups
from .test import page, workflow, datatypes, app_datas

def create_live_appdata_with_fields(app_datas):
    """
    Creates a safe live app data object that preserves all field names.
    Each table gets a single empty record to display headers in the frontend.
    """
    live_data = {}

    for table, records in app_datas.items():
        if records:
            # Take keys from the first record
            keys = records[0].keys()
        else:
            keys = []  # fallback if table has no records

        # Create a single empty record with all keys
        empty_record = {key: "" for key in keys}
        live_data[table] = [empty_record] if keys else []

    return live_data


from payments.models import PlatformUsage
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class test2(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            prompt = request.data.get("prompt", "")
            project_name = request.data.get("project_name")

            if not project_name:
                return Response(
                    {"error": "Project name is required"},
                    status=400
                )

            if Project.objects.filter(user=user, project_name=project_name).exists():
                return Response(
                    {"error": "A project name already exists."},
                    status=400
                )

            # 🔐 ATOMIC CREDIT CONSUMPTION
            with transaction.atomic():
                usage, _ = PlatformUsage.objects.get_or_create(user=user)
                usage.refresh_from_db()

                if not usage.can_use_prompt():
                    return Response(
                        {
                            "error": "NO_PROMPTS_LEFT",
                            "message": "No prompt credits left"
                        },
                        status=402  # ✅ IMPORTANT
                    )

                # ✅ CONSUME BEFORE EXPENSIVE WORK
                usage.consume_prompt()

            # 🚀 SAFE TO DO EXPENSIVE WORK BELOW

            project = Project.objects.create(
                user=user,
                project_name=project_name
            )
            project.mark_opened()

            page_with_nav = add_navbar_buttons(page)
            page_with_nav["globalPopups"] = globalPopups

            version = ProjectVersion.objects.create(
                project=project,
                version_type="preview",
                ui_schema=page_with_nav,
                workflows=workflow,
                data_types=datatypes,
                app_data=app_datas
            )

            liveappdata = BeforeDeployLiveAppData.objects.create(
                project=project,
                data=create_live_appdata_with_fields(app_datas)
            )

            return Response(
                {
                    "schema": page_with_nav,
                    "datatypes": datatypes,
                    "workflows": workflow,
                    "appdata": app_datas,

                    "project_id": project.id,
                    "project_name": project.project_name,
                    "project_slug": project.slug,
                    "liveappdata": liveappdata.data,

                    "version_type": version.version_type,
                },
                status=200
            )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=400
            )

        except Exception as e:
            print("❌ Exception in test2.post:", e)
            traceback.print_exc()
            return Response(
                {"error": "Something went wrong"},
                status=500
            )
        
import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI


def clean_json_output(text: str) -> str:
    """Cleans AI-generated output by removing code fences and stray text."""
    if not isinstance(text, str):
        text = str(text)

    text = re.sub(r"```(json|python)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()

    json_match = re.search(r"(\{[\s\S]*?\}|\[[\s\S]*?\])", text)
    if json_match:
        return json_match.group(1).strip()

    return text

def extract_structure_without_styles_for_pages(pages):
    """
    Extract schema without styles.
    Keeps hierarchy, children, dynamicData, dataFields, dataSource, typeOfContent, itemWidth.
    """

    def process_element(el):
        # Keep all relevant keys except 'style'
        keys_to_keep = [
            "id", "type", "hidden", "parentId", "indexInParent",
            "value", "dynamicData", "dataFields", "dataSource",
            "typeOfContent", "itemWidth", "children"
        ]
        simplified = {k: el[k] for k in keys_to_keep if k in el}

        # Recursively process children
        if "children" in el:
            simplified["children"] = [process_element(child) for child in el["children"]]

        return simplified

    return [process_element(page) for page in pages]


# ---------- Helper: Convert style keys to camelCase ----------
# ---------- "padding-top": 20, ----------
# ---------- "paddingTop": 20 ----------
def convert_style_keys_to_camelcase(d):
    if isinstance(d, dict):
        new_dict = {}
        for k, v in d.items():
            new_key = re.sub(r"-(\w)", lambda m: m.group(1).upper(), k)
            new_dict[new_key] = convert_style_keys_to_camelcase(v)
        return new_dict
    elif isinstance(d, list):
        return [convert_style_keys_to_camelcase(i) for i in d]
    return d

def extract_workflow_elements(pages):
    """
    Recursively extract all UI elements except excluded types.
    Keeps all keys except 'style'.
    """

    excluded_types = {
        "column-container", "row-container", "header", "banner",
        "piechart", "barchart", "linechart", "radarchart", "areachart",
        "navbar"
    }

    elements_list = []

    def process_element(el, page):
        el_type = el.get("type")

        if el_type not in excluded_types:
            # Copy everything except 'style'
            base = {k: v for k, v in el.items() if k != "style"}

            # Add page context
            base["pageId"] = page.get("id")
            base["pageName"] = page.get("name")

            elements_list.append(base)

        # Recursively process children
        for child in el.get("children", []):
            process_element(child, page)

    # Start from top-level pages
    for page in pages:
        for el in page.get("children", []):
            process_element(el, page)

    return elements_list


from .example import example_json

class GenerateSchemeAI(APIView):

    def _ask_ai(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """Call OpenAI API and return the response content."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=2500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"_ask_ai failed: {str(e)}")
    
    def post(self, request):
        user = request.user
        user_prompt = request.data.get("prompt", "").strip()
        project_name = request.data.get("project_name")

        if Project.objects.filter(user=user, project_name=project_name).exists():
            return Response(
                {"error": "A project name already exists."},
                status=400)
            
        if len(user_prompt) > 500:
            return Response(
                {"error": "Prompt too long (max 500 chars)."},
                status=400)

        try:

            ai_combined_prompt = """
You are a senior full-stack and backend architect.

App Description:
"{user_prompt}"

Task:
1. Generate exactly 4 logical main application pages.
2. Generate database tables (datatypes) and app datas for this application.

Rules:
- Pages:
    1. Do NOT include Login, Signup, Register, Authentication, or Admin pages.
    2. Return ONLY a valid JSON array of 4 page names.
- Datatypes:
    1. Include 3–7 tables relevant to the app description and pages.
    2. Each table must have:
        - "name": snake_case table name
        - "fields": array of objects with:
            - "name": camelCase field name
            - "type": one of "text", "number", "email", "image", "date", "boolean", or "reference"
            - "referenceTo": required if type is "reference" (e.g., {{ "name": "orders", "type": "reference", "referenceTo": "orders", "cardinality": "list", "relation": {{ "from": "users", "to": "orders" }} }})
            - "cardinality": "single" for primitive fields, "list" for relation fields
            - "relation": object with "from" and "to" table names for relation fields
    3. Include 2–4 sample records per table.
    4. All reference fields in app datas must point to valid records in other tables.
- Return a single JSON object with keys: "pages", "datatypes", "appDatas".
- Do NOT include markdown, explanations, or comments.
- Return JSON only — no extra text or formatting.

Format example:
{{
  "pages": ["Home", "Products", "Cart", "Orders"],
  "datatypes": [
    {{
      "name": "users",
      "fields": [
        {{"name": "name", "type": "text", "cardinality": "single"}},
        {{"name": "orders", "type": "reference", "referenceTo": "orders", "cardinality": "list", "relation": {{"from": "users", "to": "orders"}}}}
      ]
    }}
  ],
  "appDatas": {{
    "users": [
      {{"id": 1, "name": "Alice", "orders": [101, 102]}}
    ]
  }}
}}

Now generate the JSON.
""".format(user_prompt=user_prompt)

            # Step 1: AI schema
            try:
                ai_output = clean_json_output(self._ask_ai(prompt=ai_combined_prompt))
                parsed_output = json.loads(ai_output)
            except RuntimeError as e:
                return Response({"error": "AI request failed", "details": str(e)}, status=500)
            except json.JSONDecodeError as e:
                return Response({"error": "Failed to parse AI JSON", "details": str(e)}, status=500)

            parsed_output = json.loads(ai_output)

            pages = parsed_output.get("pages", [])
            datatypes = parsed_output.get("datatypes", [])
            appDatas = parsed_output.get("appDatas", {})

            # ✅ Validate AI output
            if not isinstance(pages, list) or len(pages) != 4:
                return Response({"error": "AI returned invalid pages structure"}, status=500)
            if not isinstance(datatypes, list):
                return Response({"error": "AI returned invalid datatypes structure"}, status=500)
            if not isinstance(appDatas, dict):
                return Response({"error": "AI returned invalid appDatas structure"}, status=500)
            
            # Validate field types
            valid_types = {"text", "number", "email", "image", "date", "boolean", "reference"}
            for table in datatypes:
                for field in table.get("fields", []):
                    if field.get("type") not in valid_types:
                        field["type"] = "text"


            # Assume pages = ["HomePage", "RestaurantListPage", "MenuPage", "CartPage", "CheckoutPage"]

            # step 2
            all_pages_schema = []
            generated_pages = []

            batch_size = 2
            num_pages = len(pages)

            example_ui_schema = example_json


            types = ["column-container","row-container","navbar","link","input","button","text","repeating_group",
                    "card","image","header","banner","label","dropdown","checkbox","radio",
                    "piechart","barchart","linechart","radarchart","areachart"]

            styles = ["gap","paddingTop","display","flexDirection","alignItems",
                    "paddingBottom","paddingLeft","paddingRight","backgroundColor",
                    "justifyContent","boxShadow","textDecoration","color",
                    "hoverBackgroundColor","transition","borderRadius","fontSize",
                    "fontWeight","hoverTransform","border","outline","flexGrow","cursor",
                    "marginBottom","marginTop","marginLeft","marginRight","flexWrap",
                    "overflowX","objectFit","alignSelf","textAlign"]


            for start in range(0, num_pages, batch_size):
                end = min(start + batch_size, num_pages)
                batch_pages = pages[start:end]

                # Extract important elements from previous pages if not first batch
                if start > 0:
                    important_summary = extract_structure_without_styles_for_pages(all_pages_schema)
                    important_summary_json = json.dumps(important_summary, indent=2)
                else:
                    important_summary_json = ""  # no previous pages

                for page_name in batch_pages:
                    schema_instruction = f"""
    You are an expert UI designer and front-end architect.

    Given the app description: "{user_prompt}"
    The full app will have these pages: {pages}

    Generate the UI only for the current page: "{page_name}".
    Remaining pages will be generated in the next batch.

    Use datatypes for data binding: {json.dumps(datatypes)}.

    Important Rules

    01 ONLY use element types defined in the {types}. Do NOT introduce undefined types.

    02 ONLY use style properties defined in the {styles}. Do NOT use any other CSS property.

    03 Every element must include id, type, hidden, parentId, indexInParent, style, pageId.

    04 IDs must be globally unique across all pages.

    05 pageId must match the page the element belongs to.

    06 parentId must always reference a valid existing element or null only for root page.

    07 Containers column-container, navbar, card, repeating_group must include children and must NOT include value, must NOT include dataFields, must NOT include dataSource except repeating_group, and must follow flexbox layout only.

    08 Leaf elements text, button, link, input, image, label, dropdown, checkbox, radio, piechart, barchart, linechart, radarchart, areachart must NOT include children. They may include value, may include props, may include dataFields if using dynamicData, and must include style.

    09 Interactive elements button, link, input must define behavior inside props. Allowed event keys are onClick, onChange, onSubmit.

    10 Do NOT generate content, actionType, navigationTarget, events, or any unsupported fields.

    11 Layout must use flexbox styling only. Allowed layout properties are display, flexDirection, alignItems, justifyContent, gap, paddingTop, paddingBottom, paddingLeft, paddingRight, flexWrap, flexGrow. Do NOT use x, y, absolute positioning, zIndex, or manual width or height positioning.

    12 indexInParent must control order, must have no duplicates under the same parent, and must start from 0 and increment sequentially.

    13 repeating_group must include children, must include itemWidth, must include typeOfContent, may include dataSource, must NOT include value, and only repeating_group is allowed to define dataSource.

    14 If an element uses dynamicData or displays backend-driven values, it must include dataFields and must NOT hardcode value without dataFields.

    15. Charts (linechart, barchart, piechart, radarchart, areachart)
        15.1 Every chart element must include a data object with the following mandatory fields:
            labels: an array of strings, representing x-axis or category labels.
            datasets: an array of objects, each representing a dataset. Each dataset object must include:
            label: a string, the name of the dataset
            data: an array of numeric values (matching the length of labels)
            borderColor: a color string (mandatory)
            backgroundColor: a color string (mandatory)
            borderWidth: a number (optional, default 1)
            fill: a boolean (for line/area charts only, optional, default false)
            tension: a number (for line/area charts only, optional, default 0)

        15.2 Each chart element must include style, including at least height and width. Other style properties must follow the allowed list (padding, gap, flex, etc.).
    16 Each page must contain at least 10 - 15 elements total including nested children.

    17 Do not generate extra or unsupported fields. Follow the schema strictly.

    Example UI schema for reference:

    {json.dumps(example_ui_schema, indent=2)}

    All elements from previously generated pages except Styles (if any):

    {important_summary_json}"""


                    ai_output = clean_json_output(self._ask_ai(prompt=schema_instruction))
                    try:
                        schema_dict = json.loads(ai_output)
                    except Exception as e:
                        return Response({
                            "error": f"Failed to parse AI JSON output for page {page_name}: {str(e)}",
                            "raw_output": ai_output
                        }, status=500)

                    generated_pages.extend(schema_dict.get("pages", []))
                    all_pages_schema.append(schema_dict)


            # ---------- Step 6: Combine all pages ----------
            final_schema = {
                "activePageId": 1,
                "pages": generated_pages  # already contains all pages with nested children
            }

            # ---------- Step 7: Reassign sequential page & element IDs ----------
            for idx, page in enumerate(final_schema.get("pages", []), start=1):
                page["id"] = idx

            # ---------- Step 7: Reassign sequential page & element IDs (SAFE VERSION) ----------
    # ---------- Step 7: Reassign sequential page & element IDs ----------

            old_to_new = {}
            id_counter = {"value": 1}

            def remap_elements(elements, page_id, parent_id):
                for element in elements:
                    old_id = element["id"]
                    new_id = id_counter["value"]

                    old_to_new[old_id] = new_id
                    element["id"] = new_id
                    element["pageId"] = page_id
                    element["parentId"] = parent_id

                    id_counter["value"] += 1

                    if "children" in element and element["children"]:
                        remap_elements(element["children"], page_id, new_id)


            for page_index, page in enumerate(final_schema.get("pages", []), start=1):
                page["id"] = page_index

                if "children" in page and page["children"]:
                    remap_elements(page["children"], page_index, page_index)

            # ---------- Step 8: Add global popups ----------
            # Remap popup IDs to avoid collisions
            def remap_popup_ids(elements):
                for el in elements:
                    el["id"] = id_counter["value"]
                    id_counter["value"] += 1
                    if "children" in el and el["children"]:
                        remap_popup_ids(el["children"])

            remap_popup_ids(globalPopups["children"])

            # Inject into final_schema
            final_schema["globalPopups"] = globalPopups
            # ---------- Step 8: Convert style keys ----------
            final_schema = convert_style_keys_to_camelcase(final_schema)

            
            # ---------- Step 9: Prepare workflow elements ----------
            workflow_prompt = f"""
    You are an expert front-end automation architect.

    The following JSON represents interactive UI elements from an app schema.

    App Description: "{user_prompt}"

    Pages:
    {json.dumps([{"pageId": p["id"], "pageName": p["name"]} for p in pages], indent=2)}

    Datatypes:
    {json.dumps(datatypes, indent=2)}

    UI Elements:
    {json.dumps(extract_workflow_elements(final_schema), indent=2)}

    WORKFLOW STRUCTURE (Required)

    Each workflow must strictly follow:

    {
    "id": "unique_workflow_id",
    "pageId": number,
    "pageName": "string",
    "elementId": "string or null",
    "elementType": "string or null",
    "description": "short meaningful text",
    "trigger": {{}},
    "conditions": [],
    "actions": []
    }

    TRIGGERS (Required)

    Trigger must exist and be an object.
    Only 2 types:

    1. ELEMENT TRIGGER
    Used for user interaction.

    "trigger": {
    "type": "element",
    "event": "clicked",
    "scope": "element"
    }

    Rules:
    - elementId must NOT be null
    - event allowed: "clicked"
    - scope must be "element"

    2. GENERAL TRIGGER
    Used for automatic events.

    "trigger": {
    "type": "general",
    "event": "page_loaded"
    }

    Rules:
    - elementId must be null
    - Only allowed event: "page_loaded"
    - Must not reference elementId

    WORKFLOW CONDITIONS

    Checked before actions run.
    If failed → workflow stops.
    Empty format: "conditions": []

    Allowed type:
    - current_user

    Allowed operators:
    - is logged in
    - is logged out

    ACTIONS

    - Must be array
    - Minimum 1, Maximum 2 actions
    - Execute in order
    - Each action checks its own conditions before running

    Action structure:

    {
    "id": "unique_action_id",
    "category": "navigation | account | data | element",
    "actionType": "string",
    "conditions": []
    }

    Allowed condition source:
    - current_user

    Allowed operators:
    - is logged in
    - is logged out

    NAVIGATION (category: navigation)

    Allowed actionTypes:
    - navigate (requires targetPageId)
    - refresh
    - previous

    ACCOUNT (category: account)

    Allowed actionTypes:
    - login
    - logout
    - signup
    - update_user_credentials
    - make changes to current user

    login requires:
    email, password

    signup requires:
    email, password, confirmPassword

    update_user_credentials requires:
    email, password, oldPassword, confirmPassword

    All above must use:
    {
    "source": "input_element_id in ui schema",
    "property": "value",
    "operators": [],
    "returnType": "text"
    }

    logout → no email/password

    update_user_credentials must include:
    email,password,oldPassword,confirmPassword

    update_user_credentials email, password, oldPassword, confirmPassword must have source (input element id), property is always value,

    example:
    "email": {
            "source": "9333dd38-8333-4bac-965b-1d2bd0f01af9",
            "property": "value",
            "operators": [],
            "returnType": "text"
            },
            "category": "account",
            "password": {
            "source": "e2c9d756-3afc-4480-81de-e99273ef2e9e",
            "property": "value",
            "operators": [],
            "returnType": "text"
            },
            "actionType": "update_user_credentials",
            "oldPassword": {
            "source": "e809ce29-9c2b-4ef8-9bcb-6a4d7df0ba92",
            "property": "value",
            "operators": [],
            "returnType": "text"
            },
            "confirmPassword": {
            "source": "49685088-e5ce-49f6-a38a-39704c9b686b",
            "property": "value",
            "operators": [],
            "returnType": "text"
            },


    make changes to current user must include:
    - fields (array)
    - fieldsMap (mapped to input sources)

    Field must exist in user datatype.
    fieldsMap must have that field, and that filed must have source (input element id), property is always value,

    example:
    "fields": [
            "name"
            ],
            "category": "account",
            "fieldsMap": {
            "name": {
                "source": 9103,
                "property": "value",
                "operators": [],
                "returnType": "text"
            }
            },


    DATA (category: data)

    Allowed actionTypes:
    - create

    create requires:
    - thingType (datatype table name)
    - fieldsMap (input source mapping)

    thingType is table name of above datatypes
    fieldsMap must have that field, and that filed must have source (input element id), property is always value,

    exmaple:
    "fieldsMap": {
            "name": {
                "source": "3e6a3b92-e681-47bd-b190-a0aa0332814d",
                "property": "value",
                "operators": [],
                "returnType": "text"
            }
            },
            "thingType": "categories",

    ELEMENT (category: element)
    Allowed actionTypes:
    - open_popup (requires popupId)
    - hide (requires targetElementId)
    - show (requires targetElementId)

    EXECUTION FLOW

    1. Trigger fires
    2. Workflow conditions checked
    3. Actions run in order
    4. Each action checks its own conditions

    VALIDATION RULES (STRICT)

    - trigger must exist
    - No unknown trigger types
    - No unknown actionTypes
    - Category must match actionType
    - elementId null for general trigger
    - elementId NOT null for element trigger
    - actions cannot be empty
    - No extra properties anywhere
    - Description must be short
    - Strict JSON structure

    OUTPUT

    Return ONLY a valid JSON array of workflows.
    No explanations.
    No markdown.
    No comments.
    """

            ai_workflow_output = clean_json_output(self._ask_ai(prompt=workflow_prompt))
            try:
                workflow_data = json.loads(ai_workflow_output)
            except json.JSONDecodeError as e:
                return Response({
                    "error": "Failed to parse workflow JSON",
                    "raw_output": ai_workflow_output,
                    "details": str(e)
                }, status=500)

            with transaction.atomic():
                usage, _ = PlatformUsage.objects.get_or_create(user=user)
                usage.refresh_from_db()

                if not usage.can_use_prompt():
                    return Response({"error": "NO_PROMPTS_LEFT","message": "No prompt credits left"}, status=402)

                usage.consume_prompt()
                usage.save()  # ensure consumption persists

                project = Project.objects.create(user=user, project_name=project_name)
                project.mark_opened()

                version = ProjectVersion.objects.create(
                    project=project,
                    version_type="preview",
                    ui_schema=final_schema,
                    workflows=workflow_data,
                    data_types=datatypes,
                    app_data=appDatas
                )

                liveappdata = BeforeDeployLiveAppData.objects.create(
                    project=project,
                    data=create_live_appdata_with_fields(appDatas)
                )
                        
            return Response(
                    {
                        "schema": final_schema,
                        "datatypes": datatypes,
                        "workflows": workflow_data,
                        "appdata": appDatas,

                        "project_id": project.id,
                        "project_name": project.project_name,
                        "project_slug": project.slug,
                        "liveappdata": liveappdata.data,

                        "version_type": version.version_type,
                    },
                    status=200
                )
        except ValidationError as e:
            return Response({"error": str(e)},
                            status=400)

        except Exception as e:
            print("❌ Exception in GenerateSchemeAI.post:", e)
            traceback.print_exc()
            return Response({"error": "Something went wrong"},
                            status=500)
    


# # 1. List all apps (like Bubble dashboard)
# class GeneratedAppListView(ListAPIView):
#     queryset = GeneratedApp.objects.all().order_by("-created_at")
#     serializer_class = GeneratedAppSerializer


# # 2. Retrieve one app by id (like opening in Bubble editor)
# class GeneratedAppDetailView(RetrieveAPIView):
#     queryset = GeneratedApp.objects.all()
#     serializer_class = GeneratedAppSerializer

# class GeneratedAppUpdateView(UpdateAPIView):
#     queryset = GeneratedApp.objects.all()
#     serializer_class = GeneratedAppSerializer
#     http_method_names = ["patch", "put"]

#     def perform_update(self, serializer):
#         instance = self.get_object()
#         AppVersion.objects.create(
#             app=instance,
#             concepts=instance.concepts,
#             screens=instance.screens,
#         )
#         serializer.save()

# class RollbackAppView(APIView):
#     def post(self, request, app_id, version_id):
#         try:
#             app = GeneratedApp.objects.get(pk=app_id)
#             version = AppVersion.objects.get(pk=version_id, app=app)
#         except (GeneratedApp.DoesNotExist, AppVersion.DoesNotExist):
#             return Response({"error": "App or version not found"}, status=status.HTTP_404_NOT_FOUND)

#         # ✅ overwrite current app with old version data
#         app.concepts = version.concepts
#         app.screens = version.screens
#         app.save()

#         return Response(GeneratedAppSerializer(app).data, status=status.HTTP_200_OK)
    
