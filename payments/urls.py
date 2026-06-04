from django.urls import path
from .views import *

urlpatterns = [
    # Create Razorpay order for a project
    path(
        "create/<slug:project_slug>/create-order/",
        RazorpayOrderCreateAPIView.as_view(),
        name="razorpay_order_create"
    ),

    # Complete Razorpay payment for a project
    path(
        "complete/<slug:project_slug>/payment-complete/",
        RazorpayPaymentCompleteAPIView.as_view(),
        name="razorpay_payment_complete"
    ),
    path("update-live/<slug:project_slug>/", UpdateLiveProjectAPIView.as_view(), name="update-live"),
    path(
        "platform-usage/",
        PlatformUsageAPIView.as_view(),
        name="platform-usage",
    ),

    path(
        "projects/<str:project_slug>/status-or-expire/",
        ProjectExpireAPIView.as_view(),
        name="project-expire",
        
    ),
    path(
        "platform-create-order/",
        CreatePlatformOrderAPIView.as_view(),
        name="platform-create-order",
    ),
    path(
        "platform-payment-complete/",
        CompletePlatformPaymentAPIView.as_view(),
        name="platform-payment-complete",
    ),
    path("neft-upload/", NEFTUploadView.as_view(), name="neft-upload"),
    path(
        "manual/<slug:project_slug>/",
        LiveNEFTUploadAPIView.as_view(),
        name="live-neft-upload",
    ),
]


