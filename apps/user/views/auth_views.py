from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model 
from ..serializers import *
from ...utils import OTPService
from ..services import JWTService

User = get_user_model()


class RegisterAPIView(APIView):
    """Register new normal user and send OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate recipient name from user data
            recipient_name = getattr(user, 'full_name', None) or getattr(user, 'first_name', None) or user.email.split('@')[0].title()
            
           
            # Send OTP - FIXED: Now passing recipient_name parameter
            otp_instance, email_success, email_message = OTPService.create_otp(
                email=user.email, 
                otp_type='registration',
                send_email=True,  # Explicitly set to True
                recipient_name=recipient_name
            )
            
            
            # Check if email sending was successful
            if not email_success:
                user.delete()
                return Response({'error': email_message}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'Registration successful. Please check your email for OTP.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPIView(APIView):
    """Verify OTP for registration, login, or password reset"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            otp_type = serializer.validated_data['otp_type']
            
            success, message = OTPService.verify_otp(email, otp_code, otp_type)
            if not success:
                return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
            
            return self._handle_otp_verification(email, otp_type)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _handle_otp_verification(self, email, otp_type):
        """Handle different OTP verification types"""
        if otp_type == 'registration':
            return self._handle_registration_verification(email)
        elif otp_type == 'login':
            return self._handle_login_verification(email)
        elif otp_type == 'password_reset':
            return Response({
                'message': 'OTP verified successfully. You can now proceed to reset your password.',
                'email': email 
            })

        return Response({'message': 'OTP verified successfully'})
    
    def _handle_registration_verification(self, email):
        """Activate user account after registration OTP verification"""
        try:
            user = User.objects.get(email=email)
            user.is_active = True
            user.is_verified = True
            user.save()
            
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Account verified successfully',
                **token_data
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_login_verification(self, email):
        """Complete login process after OTP verification"""
        try:
            user = User.objects.get(email=email)
            if user.is_blocked:
                return Response({'error': 'Account is blocked'}, status=status.HTTP_403_FORBIDDEN)
            
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Login successful',
                **token_data
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    """Login with email and password, enforces OTP for Admin users."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            if user.role == 'admin':
                print(f"Admin login detected for {user.email}. Sending OTP.")
                
                # Generate recipient name
                recipient_name = getattr(user, 'full_name', None) or getattr(user, 'first_name', None) or user.email.split('@')[0].title()
                
                otp_instance, email_success, email_message = OTPService.create_otp(
                    email=user.email, 
                    otp_type='login', 
                    send_email=True,
                    recipient_name=recipient_name
                )
                
                if not email_success:
                    return Response({'error': email_message}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'message': 'Admin login requires OTP verification. OTP sent to your email.',
                    'email': user.email,
                    'requires_otp': True 
                }, status=status.HTTP_202_ACCEPTED)
            
            # Original logic for non-admin users
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Login successful',
                **token_data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginOTPAPIView(APIView):
    """Request OTP for login"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = LoginOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                if user.is_blocked:
                    return Response({'error': 'Account is blocked'}, status=status.HTTP_403_FORBIDDEN)
                
                # Generate recipient name
                recipient_name = getattr(user, 'full_name', None) or getattr(user, 'first_name', None) or user.email.split('@')[0].title()
                
                
                # FIXED: Use create_otp method instead of separate create and send
                otp_instance, email_success, email_message = OTPService.create_otp(
                    email=email, 
                    otp_type='login',
                    send_email=True,
                    recipient_name=recipient_name
                )
                
                
                if not email_success:
                    return Response({'error': email_message}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({'message': 'OTP sent to your email'})
                
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """Logout user by blacklisting refresh token"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            success, message = JWTService.blacklist_token(refresh_token)
            if not success:
                return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Logged out successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshUserDataAPIView(APIView):
    """Refresh user data and generate new tokens"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if user.is_blocked:
            return Response({'error': 'Account is blocked'}, status=status.HTTP_403_FORBIDDEN)
        
        token_data = JWTService.create_tokens_for_user(user)
        
        return Response({
            'message': 'User data refreshed successfully',
            **token_data
        })