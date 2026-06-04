from django.urls import path
from .views import SecondaryUserLogoutAPIView, CreateThingAPIView, SecondaryUserCredentialsUpdateAPIView,SecondaryUserSessionAPIView,SecondaryUserSignupAPIView, SecondaryUserLoginAPIView ,SecondaryUserUpdateAPIView
urlpatterns = [
        path('projects/session-user/<str:project_slug>/', SecondaryUserSessionAPIView.as_view()),

    path(
        'projects/<slug:project_slug>/pcl-user-login/', 
        SecondaryUserLoginAPIView.as_view(), 
        name='pcl-user-login'
    ),
    path(
        'projects/<slug:project_slug>/logout/',
        SecondaryUserLogoutAPIView.as_view(),
        name='pcl-user-logout'
    ),
    path(
        'projects/<slug:project_slug>/pcl-user-signup/', 
        SecondaryUserSignupAPIView.as_view(), 
        name='pcl-user-login'
    ),

    path(
        "projects/<slug:project_slug>/pcl-user-update/",
        SecondaryUserUpdateAPIView.as_view(),
        name="secondary-user-update"
    ),
    path(
"projects/<slug:project_slug>/pcl-user-credentials-update/",
  SecondaryUserCredentialsUpdateAPIView.as_view(),
),
    path(
        "projects/<slug:project_slug>/data/<str:thing_type>/",
        CreateThingAPIView.as_view(),
        name="create-thing"
    ),
    
]
