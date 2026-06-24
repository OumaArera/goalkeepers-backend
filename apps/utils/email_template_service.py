import logging
from django.conf import settings # pyright: ignore[reportMissingModuleSource]
from typing import Tuple

# Set up logging
logger = logging.getLogger(__name__)


class EmailTemplateService:
    """Service for generating email templates"""
    
    @staticmethod
    def get_otp_email_content(code: str, otp_type: str) -> Tuple[str, str, str]:
        """
        Generate email subject and content for OTP
        
        Args:
            code: OTP code
            otp_type: Type of OTP (registration, login, password_reset)
            
        Returns:
            Tuple of (subject, html_content, plain_content)
        """
        otp_expiry = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        
        # Subject mapping
        subject_map = {
            'registration': 'Verify Your Goalkeepers Alliance Account',
            'login': 'Your Goalkeepers Alliance Login Code',
            'password_reset': 'Reset Your Goalkeepers Alliance Password'
        }
        
        subject = subject_map.get(otp_type, 'Your Goalkeepers Alliance Verification Code')
        
        # Determine the primary site URL
        site_url = getattr(settings, 'PRIMARY_SITE_URL', 'https://dashboard.goalkeepersalliance.org')
        fallback_url = getattr(settings, 'FALLBACK_SITE_URL', 'https://admin.goalkeepersalliance.org')
        
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: #f4f4f4;
                }}
                .container {{ 
                    max-width: 600px; 
                    margin: 0 auto; 
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{ 
                    background-color: #007bff; 
                    color: white; 
                    padding: 30px 20px; 
                    text-align: center; 
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 300;
                }}
                .content {{ 
                    padding: 40px 30px; 
                    background-color: white;
                }}
                .content h2 {{
                    color: #333;
                    margin-bottom: 20px;
                    font-size: 24px;
                }}
                .content p {{
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}
                .otp-code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #007bff; 
                    text-align: center; 
                    padding: 25px; 
                    background-color: #f8f9fa;
                    border-radius: 6px;
                    margin: 25px 0;
                    letter-spacing: 3px;
                }}
                .footer {{ 
                    text-align: center; 
                    color: #999; 
                    font-size: 14px; 
                    padding: 20px 30px; 
                    background-color: #f8f9fa;
                    border-top: 1px solid #e9ecef;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Goalkeeper Alliance</h1>
                </div>
                <div class="content">
                    <h2>Your Verification Code</h2>
                    <p>Your Goalkeeper Alliance verification code is:</p>
                    <div class="otp-code">{code}</div>
                    <p>This code will expire in <strong>{otp_expiry} minutes</strong>.</p>
                    <div class="warning">
                        <p><strong>Security Note:</strong> If you didn't request this code, please ignore this email and ensure your account is secure.</p>
                    </div>
                </div>
                <div class="footer">
                    <p>Best regards,<br><strong>Goalkeepers Alliance Team</strong></p>
                    <p style="margin-top: 15px; font-size: 12px;">
                        This is an automated message, please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        plain_content = f"""
        Your Goalkeeper Alliance verification code is: {code}
        
        This code will expire in {otp_expiry} minutes.
        
        If you didn't request this code, please ignore this email and ensure your account is secure.
        
        Best regards,
        Goalkeeper Alliance Team
        
        ---
        This is an automated message, please do not reply to this email.
        """
        
        return subject, html_content.strip(), plain_content.strip()

   
class PasswordTemplateService:
    
    @staticmethod
    def get_password_email_content(
        password: str,
        recipient_name: str,
        is_admin_created: bool = True
    ) -> Tuple[str, str, str]:

        login_url = getattr(
            settings,
            "DASHBOARD_LOGIN_URL",
            "https://dashboard.goalkeepersalliance.org/login"
        )

        if is_admin_created:
            subject = "Welcome to Goalkeepers Alliance! Your Account Details"
            intro_message = (
                f"Hello {recipient_name}, your Goalkeepers Alliance account has been "
                f"created by an administrator. Below are your temporary login details."
            )
        else:
            subject = "Your Goalkeepers Alliance Password Has Been Reset"
            intro_message = (
                f"Hello {recipient_name}, your Goalkeepers Alliance password has been reset. "
                f"Below is your new temporary password."
            )

        note_message = "Please log in immediately and change your password."

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{subject}</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
                <h2>{subject}</h2>
                <p>{intro_message}</p>

                <p><strong>Your temporary password:</strong></p>
                <div style="font-size: 22px; font-weight: bold; padding: 15px; background: #f8f9fa; text-align: center;">
                    {password}
                </div>

                <p style="margin-top: 25px;">
                    👉 <a href="{login_url}" target="_blank">
                        Click here to log in to your account
                    </a>
                </p>

                <p style="color: #dc3545; font-weight: bold;">
                    {note_message}
                </p>

                <hr>
                <p style="font-size: 12px; color: #777;">
                    This is a sensitive email. Do not share this password with anyone.
                </p>

                <p>
                    Best regards,<br>
                    <strong>Goalkeepers Alliance Team</strong>
                </p>
            </div>
        </body>
        </html>
        """

        plain_content = f"""
        {subject}

        {intro_message}

        Temporary password:
        {password}

        Login here:
        {login_url}

        {note_message}

        ---
        This is a sensitive email. Do not share this password with anyone.
        """

        return subject, html_content.strip(), plain_content.strip()

    @staticmethod
    def get_password_email_content(password: str, recipient_name: str, is_admin_created: bool = True) -> Tuple[str, str, str]:
        # ... (Implementation as provided in the prompt)
        if is_admin_created:
            subject = 'Welcome to Goalkeepers Alliance! Your Account Details'
            intro_message = f"Hello {recipient_name}, your Goalkeepers Alliance account has been created by an administrator. Here are your temporary login details."
            note_message = "Please log in immediately and **change your password**."
        else:
            subject = 'Your Goalkeepers Alliance Password Has Been Reset'
            intro_message = f"Hello {recipient_name}, your Goalkeepers Alliance password has been reset by an administrator (or automatically). Here is your new temporary password."
            note_message = "For security, we recommend you **change your password** after logging in."
        
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                /* Reuse styles from OTP template */
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background-color: #007bff; color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 300; }}
                .content {{ padding: 40px 30px; background-color: white; }}
                .content h2 {{ color: #333; margin-bottom: 20px; font-size: 24px; }}
                .content p {{ color: #666; line-height: 1.6; margin-bottom: 15px; }}
                .password-code {{ 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #007bff; 
                    text-align: center; 
                    padding: 20px; 
                    background-color: #f8f9fa;
                    border-radius: 6px;
                    margin: 25px 0;
                    letter-spacing: 2px;
                }}
                .footer {{ text-align: center; color: #999; font-size: 14px; padding: 20px 30px; background-color: #f8f9fa; border-top: 1px solid #e9ecef; }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Goalkeepers Alliance</h1>
                </div>
                <div class="content">
                    <h2>{subject}</h2>
                    <p>{intro_message}</p>
                    <p>Your new temporary password is:</p>
                    <div class="password-code"><strong>{password}</strong></div>
                    <p style="text-align: center; font-size: 16px; font-weight: bold; color: #dc3545;">{note_message}</p>
                    <div class="warning">
                        <p><strong>Security Note:</strong> This is a sensitive email. Do not share this password with anyone.</p>
                    </div>
                </div>
                <div class="footer">
                    <p>Best regards,<br><strong>Goalkeepers Alliance Team</strong></p>
                    <p style="margin-top: 15px; font-size: 12px;">
                        This is an automated message, please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        plain_content = f"""
        {subject}
        
        {intro_message}
        
        Your new temporary password is: {password}
        
        {note_message}
        
        ---
        Security Note: This is a sensitive email. Do not share this password with anyone.
        
        Best regards,
        Goalkeepers Alliance Team
        
        ---
        This is an automated message, please do not reply to this email.
        """
        
        return subject, html_content.strip(), plain_content.strip()