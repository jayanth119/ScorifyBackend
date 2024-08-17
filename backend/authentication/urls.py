from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from .views import RegisterView,LoginView,ForgotPasswordView,ChangePasswordView,TenantProfileSetupView, AgentProfileSetupView, LandlordProfileSetupView
from django.conf.urls.static import static
urlpatterns=[
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('signup/',RegisterView.as_view(),name="signup"),
   path("login/",LoginView.as_view(),name="login"),
   path("forgot-password/",ForgotPasswordView.as_view(),name="forgot_password"),
   path("change-password/<uuid:id>/",ChangePasswordView.as_view(),name="forgot_password"),

path('tenant/profile-setup/', TenantProfileSetupView.as_view(), name='tenant-profile-setup'),
    path('agent/profile-setup/', AgentProfileSetupView.as_view(), name='agent-profile-setup'),
    path('landlord/profile-setup/', LandlordProfileSetupView.as_view(), name='landlord-profile-setup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


