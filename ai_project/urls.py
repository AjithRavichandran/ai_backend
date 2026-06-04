from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Custom auth routes (signup, login, refresh, logout)
    path("api/auth/", include("authentication.urls")),

    # ✅ Optional built-in JWT verification endpoint
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # ✅ Your main app routes
    path("api/generate/", include("generate.urls")),
    path("api/secondary_user/", include("secondary_user.urls")),
    path("api/payments/", include("payments.urls")),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)