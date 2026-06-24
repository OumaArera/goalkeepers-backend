from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response 
from django.contrib.auth import get_user_model

from ..serializers import *
from ...utils import *
from ..services import JWTService

User = get_user_model()


class ChangePasswordAPIView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            if not self._verify_old_password(user, serializer.validated_data['old_password']):
                return Response({'error': 'Old password is incorrect'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            self._update_password(user, serializer.validated_data['new_password'])
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Password changed successfully',
                **token_data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _verify_old_password(self, user, old_password):
        """Verify the old password is correct"""
        return user.check_password(old_password)
    
    def _update_password(self, user, new_password):
        """Update user password and save"""
        user.set_password(new_password)
        user.save()


class ForgotPasswordAPIView(APIView):
    """
    Reset password directly and email the new password to the user.
    No authentication required.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=True)

            if user.is_blocked:
                return Response(
                    {'error': 'Account is blocked'},
                    status=status.HTTP_403_FORBIDDEN
                )

            new_password = generate_random_password()

            user.set_password(new_password)
            user.save()

            EmailService.send_forgot_password_email(
                user_email=user.email,
                recipient_name=user.get_full_name() or user.email,
                generated_password=new_password
            )


            # 4. (Optional) Generate JWT tokens
            token_data = JWTService.create_tokens_for_user(user)

            return Response(
                {
                    'message': 'A new password has been sent to your email.',
                    **token_data
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ResetPasswordAPIView(APIView):
    """Reset password using OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            # Verify OTP first
            if not self._verify_reset_otp(email, otp_code):
                return Response({'error': 'Invalid or expired OTP'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            return self._complete_password_reset(email, new_password)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _verify_reset_otp(self, email, otp_code):
        """Verify the password reset OTP"""
        success, message = OTPService.verify_otp(email, otp_code, 'password_reset')
        return success
    
    def _complete_password_reset(self, email, new_password):
        """Complete the password reset process"""
        try:
            user = User.objects.get(email=email)
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Generate new tokens after password reset
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Password reset successfully',
                **token_data
            })
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


class PasswordStrengthAPIView(APIView):
    """Check password strength and requirements"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        password = request.data.get('password', '')
        
        if not password:
            return Response({'error': 'Password is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        strength_analysis = self._analyze_password_strength(password)
        
        return Response({
            'password_strength': strength_analysis,
            'is_valid': strength_analysis['score'] >= 3,
            'requirements_met': strength_analysis['requirements_met']
        })
    
    def _analyze_password_strength(self, password):
        """Analyze password strength and return detailed feedback"""
        import re
        
        requirements = {
            'length': len(password) >= 8,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        score = sum(requirements.values())
        
        strength_levels = {
            0: 'Very Weak',
            1: 'Very Weak', 
            2: 'Weak',
            3: 'Fair',
            4: 'Good',
            5: 'Strong'
        }
        
        feedback = []
        if not requirements['length']:
            feedback.append('Password must be at least 8 characters long')
        if not requirements['uppercase']:
            feedback.append('Include at least one uppercase letter')
        if not requirements['lowercase']:
            feedback.append('Include at least one lowercase letter')
        if not requirements['digit']:
            feedback.append('Include at least one number')
        if not requirements['special']:
            feedback.append('Include at least one special character')
        
        return {
            'score': score,
            'strength': strength_levels[score],
            'requirements_met': requirements,
            'feedback': feedback,
            'length': len(password)
        }
    
class SetNewPasswordAPIView(APIView):
    """Set new password after successful OTP verification"""
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data) 
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            return self._complete_password_reset(email, new_password)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _complete_password_reset(self, email, new_password):
        """Complete the password reset process"""
        try:
            user = User.objects.get(email=email)
            
            user.set_password(new_password)
            user.save()
            
            token_data = JWTService.create_tokens_for_user(user)
            
            return Response({
                'message': 'Password reset successfully',
                **token_data
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)