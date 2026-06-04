from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from payments.models import PlatformUsage

# ---------------------- SIGNUP ---------------------- #
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ CREATE PLATFORM USAGE (2 free prompts start here)
        PlatformUsage.objects.create(user=user)

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )


# ---------------------- LOGIN ---------------------- #
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    """
    Logs user in, returns access token in JSON,
    and sets refresh token as HttpOnly cookie (for 'forever login').
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response(
            {
                "access": access_token,
                "refresh": str(refresh),  # ✅ include this!
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )

        # ✅ Set refresh token as secure HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,  # ⚠️ Change to True in production
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,  # 7 days
        )

        return response


# ---------------------- REFRESH ACCESS TOKEN ---------------------- #
class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token found"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = Response({"access": new_access_token}, status=status.HTTP_200_OK)

            # Optional rolling session
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,  # ✅ True in production
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
            )
            return response

        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

# ---------------------- LOGOUT ---------------------- #
class LogoutAPIView(APIView):
    """
    Logs user out by deleting refresh token cookie.
    """

    def post(self, request):
        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("refresh_token")
        return response



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers

# Serializer including subscription info
class UserSerializer(serializers.ModelSerializer):
    liveusageplan = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "liveusageplan"]

    def get_liveusageplan(self, obj):
        return []  # temporary placeholder
        

# views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer


# views.py
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        project_slug = request.query_params.get("project_slug")

        serializer = UserSerializer(
            request.user,
            context={"project_slug": project_slug}
        )

        return Response(serializer.data)


# accounts/views.py
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    """
    Send password reset email using Gmail SMTP
    """
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}/"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
    

    # accounts/views.py
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    """
    Reset password using uid and token
    """
    def post(self, request, uid, token):
        password = request.data.get("password")
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)