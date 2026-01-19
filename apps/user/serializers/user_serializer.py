from rest_framework import serializers 
from django.contrib.auth import authenticate 
from django.contrib.auth.password_validation import validate_password 
from ..models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'role', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone'),
            role=validated_data['role'],
            password=validated_data['password'],
            is_active=False 
        )
        return user



class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    otp_type = serializers.ChoiceField(choices=OTP.OTP_TYPES)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if user.is_blocked:
                raise serializers.ValidationError('Account is blocked.')
            if not user.is_verified:
                raise serializers.ValidationError('Account not verified.')
            attrs['user'] = user
        return attrs


class LoginOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'full_name', 
                 'phone', 'role', 'is_verified', 'is_blocked',  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class BlockUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    block = serializers.BooleanField()


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for admin to create a user. 
    Excludes password since it will be auto-generated and emailed.
    Allows admin to set the role explicitly.
    """
    class Meta:
        model = User
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'phone', 
            'role'
        )
        extra_kwargs = {
            'role': {'required': True}
        }

    def validate_role(self, value):
        return value


class TargetEmailSerializer(serializers.Serializer):
    """Simple serializer to validate an email field for admin-initiated actions."""
    email = serializers.EmailField()

class RegistrationRequestSerializer(serializers.Serializer):
    """Serializer for requesting a user to register"""
    
    recipient_email = serializers.EmailField(
        required=True,
        max_length=255,
        error_messages={
            'required': 'Recipient email is required.',
            'invalid': 'Enter a valid recipient email address.'
        }
    )
    recipient_name = serializers.CharField(
        required=True,
        max_length=255,
        error_messages={'required': 'Recipient name is required.'}
    )

class SetNewPasswordSerializer(serializers.Serializer):
        email = serializers.EmailField()
        new_password = serializers.CharField()
        confirm_new_password = serializers.CharField()
        def validate(self, data):
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError("Passwords do not match.")
            return data