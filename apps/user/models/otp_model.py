from django.db import models
from django.utils import timezone 
import uuid

class OTP(models.Model):
    OTP_TYPES = [
        ('registration', 'Registration'),
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
        ('forgot_password', 'Forgot Password'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=15, choices=OTP_TYPES)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.email} ({self.otp_type})"
    
    class Meta:
        db_table = 'auth_otp'
        ordering = ['-created_at']