from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model
from ...utils import *
from ..serializers import *

User = get_user_model()


class AdminUserCreateAPIView(APIView):
    """Create a new 'admin' user with a generated password."""
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        # if request.user.role != 'admin':
        #     return Response({'error': 'Permission denied. Only admins can create admin users.'}, 
        #                     status=status.HTTP_403_FORBIDDEN)
        
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            
            validated_fields = serializer.validated_data.copy()
            
            new_password = generate_random_password()
            
            try:
                user = User.objects.create_user(
                    password=new_password, 
                    is_verified=True, 
                    is_active=True,
                    **validated_fields 
                )
                
                recipient_name = getattr(user, 'full_name', None) or user.email.split('@')[0].title()
                email_success, email_message = EmailService.send_generated_password_email(
                    email=user.email,
                    password=new_password,
                    recipient_name=recipient_name,
                    is_admin_created=True
                )
                
                if not email_success:
                    print(f"CRITICAL: Failed to send initial password email for {user.email}. Error: {email_message}")
                    return Response({'error': f'Admin created, but failed to send password email: {email_message}'}, 
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({
                    'message': 'Admin user created successfully. Temporary password sent to their email.',
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
                
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'An unexpected error occurred: {str(e)}'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPasswordResetAPIView(APIView):
    """Admin-initiated password reset for any user."""
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        # if request.user.role != 'admin':
        #     return Response({'error': 'Permission denied. Only admins can reset user passwords.'}, 
        #                     status=status.HTTP_403_FORBIDDEN)
        
        serializer = TargetEmailSerializer(data=request.data) 
        if serializer.is_valid():
            target_email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=target_email)
                
                new_password = generate_random_password()
                
                user.set_password(new_password)
                user.save()
                
                recipient_name = getattr(user, 'full_name', None) or user.email.split('@')[0].title()
                email_success, email_message = EmailService.send_generated_password_email(
                    email=user.email,
                    password=new_password,
                    recipient_name=recipient_name,
                    is_admin_created=False
                )

                if not email_success:
                    return Response({'error': f'Password reset in DB, but failed to send email: {email_message}'}, 
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({
                    'message': f'Password for {target_email} has been reset. New password sent to their email.'
                })
                
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': f'An unexpected error occurred: {str(e)}'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordAuthAPIView(APIView):
    """Authenticated user changes their own password."""
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user = request.user
        
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            
            return Response({'message': 'Password changed successfully. Please log in again.'},
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)