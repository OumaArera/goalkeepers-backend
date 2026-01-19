from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model
from ..middlewares import AllUsers
from ..serializers import *
from ...utils import EmailService

User = get_user_model()

class RegistrationRequestAPIView(APIView):
    """
    Sends an email to a non-existent user, asking them to register 
    to facilitate a vehicle transfer.
    """
    permission_classes = [AllUsers] 

    def post(self, request):
        serializer = RegistrationRequestSerializer(data=request.data)
        if serializer.is_valid():
            recipient_email = serializer.validated_data['recipient_email']
            recipient_name = serializer.validated_data['recipient_name']
            
            sender = request.user
            sender_name = getattr(sender, 'full_name', None) or getattr(sender, 'first_name', None) or sender.email.split('@')[0].title()
            
            success, message = EmailService.send_registration_request_email(
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                sender_name=sender_name
            )
            
            if success:
                return Response({
                    'message': 'Registration request email sent successfully.',
                    'recipient_email': recipient_email
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send registration request email.',
                    'detail': message
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
