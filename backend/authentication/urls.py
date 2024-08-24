from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
from django.conf import settings
from .views import (RegisterView,LoginView,ForgotPasswordView,ChangePasswordView, AgentProfileSetupView, LandlordProfileSetupView , 
                    SendOTPView ,VerifyOTPView , CustomTokenRefreshView,TenantRegisterView , TenantOTPVerificationView
                    )
from django.conf.urls.static import static
urlpatterns=[
   path('custom/token/refresh/', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
   path('signup/',RegisterView.as_view(),name="signup"),
   path("login/",LoginView.as_view(),name="login"),
   path("forgot-password/",ForgotPasswordView.as_view(),name="forgot_password"),
   path("change-password/<uuid:id>/",ChangePasswordView.as_view(),name="forgot_password"),
    path('agent/profile-setup/', AgentProfileSetupView.as_view(), name='agent-profile-setup'),
    path('landlord/profile-setup/', LandlordProfileSetupView.as_view(), name='landlord-profile-setup'),
    path('sendotp' , SendOTPView.as_view() , name="send-otp"),
    path('verifyotp' ,  VerifyOTPView.as_view() , name='verify-otp'), 
    path('tenant/signup/'  , TenantRegisterView.as_view() , name='tenant_signup') , 
    path('tenant/verifyotp' , TenantOTPVerificationView.as_view()  , name="tenant_otp"), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


