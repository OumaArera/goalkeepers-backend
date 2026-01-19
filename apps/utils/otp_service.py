import random
import string
import logging
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from typing import Tuple
from ..user.models import OTP
from .email_service import EmailService
from .email_template_service import EmailTemplateService

# Set up logging
logger = logging.getLogger(__name__)


class OTPService:
    """Service for OTP generation, verification, and email sending"""
    
    @staticmethod
    def generate_otp_code(length: int = 6) -> str:
        
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def create_otp(email: str, otp_type: str, send_email: bool = True, recipient_name: str = None) -> Tuple[OTP, bool, str]:
        
        
        # Delete existing unused OTPs for this email and type
        deleted_count = OTP.objects.filter(
            email=email,
            otp_type=otp_type,
            is_used=False
        ).count()
        
        OTP.objects.filter(
            email=email,
            otp_type=otp_type,
            is_used=False
        ).delete()
        
        print(f"Deleted {deleted_count} existing unused OTPs")
        
        # Generate new OTP
        code = OTPService.generate_otp_code()
        logger.info(f"OTP Code Generated: {code} for {email}")
        print(f"Generated OTP Code: {code}")
        
        expires_at = timezone.now() + timedelta(
            minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        )
        
        otp = OTP.objects.create(
            email=email,
            code=code,
            otp_type=otp_type,
            expires_at=expires_at
        )
        
        logger.info(f"OTP created in database for {email} (type: {otp_type})")
        print(f"OTP saved to database with ID: {otp.id}")
        
        # Send email if requested
        email_success = True
        email_message = "Email not sent (send_email=False)"
        
        if send_email:
            print("Attempting to send OTP email...")
            
            # Generate recipient name if not provided
            if not recipient_name:
                recipient_name = email.split('@')[0].title()
                print(f"Generated recipient name: {recipient_name}")
            
            email_success, email_message = OTPService.send_otp_email(
                email=email,
                code=code,
                otp_type=otp_type,
                recipient_name=recipient_name
            )
            
            if email_success:
                logger.info(f"OTP email sent successfully to {email}")
                print("✅ OTP email sent successfully")
            else:
                logger.error(f"Failed to send OTP email to {email}: {email_message}")
                print(f"❌ Failed to send OTP email: {email_message}")
        else:
            print("Email sending skipped (send_email=False)")
        
        print(f"=== OTPService.create_otp result ===")
        print(f"OTP Instance: {otp}")
        print(f"Email Success: {email_success}")
        print(f"Email Message: {email_message}")
        print("=====================================\n")
        
        return otp, email_success, email_message
    
    @staticmethod
    def create_and_send_otp(email: str, otp_type: str, recipient_name: str = None) -> Tuple[bool, str, str]:
        """
        Convenience method to create OTP and send email
        
        Args:
            email: User's email address
            otp_type: Type of OTP
            recipient_name: Recipient's name (optional)
            
        Returns:
            Tuple of (success: bool, message: str, otp_code: str)
        """
        try:
            otp, email_success, email_message = OTPService.create_otp(
                email=email,
                otp_type=otp_type,
                send_email=True,
                recipient_name=recipient_name
            )
            
            if email_success:
                return True, "OTP created and sent successfully", otp.code
            else:
                return False, f"OTP created but email failed: {email_message}", otp.code
                
        except Exception as e:
            logger.error(f"Error creating and sending OTP for {email}: {str(e)}")
            return False, f"Failed to create OTP: {str(e)}", ""
    
    @staticmethod
    def verify_otp(email: str, code: str, otp_type: str) -> Tuple[bool, str]:
        """
        Verify OTP code
        
        Args:
            email: User's email address
            code: OTP code to verify
            otp_type: Type of OTP
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            otp = OTP.objects.get(
                email=email,
                code=code,
                otp_type=otp_type,
                is_used=False
            )
            
            if otp.is_expired():
                logger.warning(f"Expired OTP verification attempt for {email}")
                return False, "OTP has expired"
            
            # Mark as used
            otp.is_used = True
            otp.save()
            
            logger.info(f"OTP verified successfully for {email}")
            return True, "OTP verified successfully"
            
        except OTP.DoesNotExist:
            logger.warning(f"Invalid OTP verification attempt for {email}")
            return False, "Invalid OTP code"
    
    @staticmethod
    def send_otp_email(email: str, code: str, otp_type: str, recipient_name: str = None) -> Tuple[bool, str]:
        """
        Send OTP via email using email service
        FIXED: Added more debugging and proper error handling
        
        Args:
            email: Recipient's email address
            code: OTP code to send
            otp_type: Type of OTP
            recipient_name: Recipient's name (optional)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            print(f"\n=== OTPService.send_otp_email called ===")
            print(f"Email: {email}")
            print(f"Code: {code}")
            print(f"OTP Type: {otp_type}")
            print(f"Recipient Name: {recipient_name}")
            
            logger.info(f"Attempting to send OTP email to {email} for {otp_type}")
            
            # Generate email content
            print("Generating email content...")
            subject, html_content, plain_content = EmailTemplateService.get_otp_email_content(code, otp_type)
            
            # Use email address as name if not provided
            if not recipient_name:
                recipient_name = email.split('@')[0].title()
                print(f"Generated recipient name: {recipient_name}")
            
            logger.info(f"Email content prepared - Subject: {subject}")
            print(f"Email subject: {subject}")
            
            # Send email
            print("Calling EmailService.send_email...")
            success, message = EmailService.send_email(
                recipient_email=email,
                recipient_name=recipient_name,
                subject=subject,
                html_content=html_content,
                plain_content=plain_content
            )
            
            print(f"EmailService.send_email result: success={success}, message={message}")
            
            if success:
                logger.info(f"OTP email sent successfully to {email}")
                print("✅ OTP email sent successfully via EmailService")
            else:
                logger.error(f"Failed to send OTP email to {email}: {message}")
                print(f"❌ Failed to send OTP email via EmailService: {message}")
            
            print("=== send_otp_email completed ===\n")
            
            return success, message
            
        except Exception as e:
            logger.error(f"Error sending OTP email to {email}: {str(e)}")
            print(f"❌ Exception in send_otp_email: {str(e)}")
            return False, f"Failed to send OTP email: {str(e)}"


def has_permission(user, required_roles):
    """Check if user has required role permissions"""
    if not user.is_authenticated:
        return False
    
    if user.is_blocked:
        return False
    
    if not user.is_verified and user.role == 'normal_user':
        return False
    
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    
    return user.role in required_roles or user.is_superuser