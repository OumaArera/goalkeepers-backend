import logging
import requests
from django.conf import settings 
from django.core.mail import EmailMultiAlternatives 
from typing import Tuple
from ..utils.email_template_service import *


logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails using different providers"""
    
    @staticmethod
    def send_email_smtp(recipient_email: str, recipient_name: str, subject: str, 
                       html_content: str, plain_content: str = None) -> Tuple[bool, str]:
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@goalkeepersalliance.org')
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_content or "Please view this email in HTML format.",
                from_email=from_email,
                to=[f'"{recipient_name}" <{recipient_email}>']
            )
            
            email.attach_alternative(html_content, "text/html")
            
            result = email.send(fail_silently=False)
            
            if result == 1:
                logger.info(f"Email sent successfully to {recipient_email}")
                return True, "Email sent successfully"
            else:
                logger.error(f"Failed to send email to {recipient_email}: No messages sent")
                return False, "Failed to send email"
                
        except Exception as e:
            logger.error(f"SMTP email sending error for {recipient_email}: {str(e)}")
            return False, f"Email service error: {str(e)}"
    
    @staticmethod
    def send_email_api(recipient_email: str, recipient_name: str, subject: str, 
                      html_content: str) -> Tuple[bool, str]:
        try:
            logger.info(f"Sending email via API to {recipient_email}")
            print(f"Sending email via API to {recipient_email}") 
            
            email_payload = {
                "sender": {
                    "email": getattr(settings, 'EMAIL_SENDER_ID', 'no-reply@goalkeepersalliance.org'), 
                    "name": getattr(settings, 'EMAIL_SENDER_NAME', 'Goalkeepers Alliance')
                },
                "to": [{"email": recipient_email, "name": recipient_name}],
                "subject": subject,
                "htmlContent": html_content
            }
            
            headers = {
                "accept": "application/json",
                "api-key": settings.EMAIL_API_KEY,
                "content-type": "application/json"
            }
            
            response = requests.post(
                settings.EMAIL_API_URL, 
                json=email_payload, 
                headers=headers
            )
            
            if response.status_code == 201:
                logger.info(f"Email sent successfully to {recipient_email} via API")
                return True, "Email sent successfully"
            else:
                logger.error(f"API email failed for {recipient_email}: {response.status_code} - {response.text}")
                return False, f"Email API error: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"API email sending error for {recipient_email}: {str(e)}")
            return False, f"Email API service error: {str(e)}"
    
    @staticmethod
    def send_email(recipient_email: str, recipient_name: str, subject: str, 
                  html_content: str, plain_content: str = None) -> Tuple[bool, str]:
        logger.info(f"Attempting to send email to {recipient_email}")
        
        use_api = getattr(settings, 'USE_EMAIL_API', False)
        has_api_key = hasattr(settings, 'EMAIL_API_KEY') and getattr(settings, 'EMAIL_API_KEY', '')
        has_api_url = hasattr(settings, 'EMAIL_API_URL') and getattr(settings, 'EMAIL_API_URL', '')
        
        if use_api and has_api_key and has_api_url:
            api_success, api_message = EmailService.send_email_api(
                recipient_email, recipient_name, subject, html_content
            )
            
            if api_success:
                return api_success, api_message
            else:
                logger.warning(f"API email failed, attempting SMTP fallback: {api_message}")
        
        email_backend = getattr(settings, 'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
        
        if 'console' in email_backend or 'dummy' in email_backend:
            logger.info(f"Backend '{email_backend}': Email notification simulated for {recipient_email}")
            return True, f"Email notification simulated ({email_backend})"
        else:
            return EmailService.send_email_smtp(recipient_email, recipient_name, subject, html_content, plain_content)

    @staticmethod
    def send_generated_password_email(email: str, password: str, recipient_name: str, is_admin_created: bool = False) -> Tuple[bool, str]:
        """
        Generates password email content and sends it.
        
        Args:
            email: Recipient's email address.
            password: The temporary password to be sent.
            recipient_name: Recipient's name.
            is_admin_created: True if this is a new account created by an admin.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        logger.info(f"Attempting to send generated password email to {email}")
        
        try:
            subject, html_content, plain_content = PasswordTemplateService.get_password_email_content(
                password=password,
                recipient_name=recipient_name,
                is_admin_created=is_admin_created
            )
        except Exception as e:
            logger.error(f"Error generating password email template for {email}: {str(e)}")
            return False, f"Error generating email template: {str(e)}"

        return EmailService.send_email(
            recipient_email=email,
            recipient_name=recipient_name,
            subject=subject,
            html_content=html_content,
            plain_content=plain_content
        )
    
    @staticmethod
    def send_registration_request_email(recipient_email: str, recipient_name: str, sender_name: str) -> Tuple[bool, str]:
        """
        Generates and sends the user registration request email for vehicle transfer.
        """
        logger.info(f"Attempting to send registration request email to {recipient_email} by {sender_name}")

        try:
            subject, html_content, plain_content = EmailTemplateService.get_registration_request_content(
                recipient_name=recipient_name,
                sender_name=sender_name
            )
        except Exception as e:
            logger.error(f"Error generating registration request email template for {recipient_email}: {str(e)}")
            return False, f"Error generating email template: {str(e)}"

        return EmailService.send_email(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            subject=subject,
            html_content=html_content,
            plain_content=plain_content
        )