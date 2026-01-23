from django.urls import path 
from rest_framework_simplejwt.views import TokenRefreshView # type: ignore
from .services import CustomTokenObtainPairView
from .views import *



urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('register-request/', RegistrationRequestAPIView.as_view(), name='register_request'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-otp/', LoginOTPAPIView.as_view(), name='login_otp'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh-user-data/', RefreshUserDataAPIView.as_view(), name='refresh_user_data'),
    
    # Token management
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Users
    path('users/', UserViewSet.as_view(), name='users'),
    
    # Password management
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('set-new-password/', SetNewPasswordAPIView.as_view(), name='set_new_password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('password-strength/', PasswordStrengthAPIView.as_view(), name='password_strength'),

    path('admin/create-user/', AdminUserCreateAPIView.as_view(), name='admin_create_user'),
    path('admin/reset-password/', AdminPasswordResetAPIView.as_view(), name='admin_reset_password'), 
    path('change-password-auth/', ChangePasswordAuthAPIView.as_view(), name='change_password_auth'),
]