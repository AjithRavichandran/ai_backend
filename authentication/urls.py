from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshAccessTokenView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path("me/", MeAPIView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<int:uid>/<str:token>/", ResetPasswordView.as_view(), name="reset-password"),
  
]
