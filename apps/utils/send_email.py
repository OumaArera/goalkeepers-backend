from config import settings
from django.core.mail import EmailMultiAlternatives

def send_email(recipient_email, recipient_name, subject, html_content):
    """Sends Email using SMTP with domain email"""
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="", 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[f'"{recipient_name}" <{recipient_email}>'],
        )
        
        # Attach HTML content
        email.attach_alternative(html_content, "text/html")
        
        email.send(fail_silently=False)
        
        return True
    except Exception as ex:
        print(f"Failed to send email: {ex}")
        return False