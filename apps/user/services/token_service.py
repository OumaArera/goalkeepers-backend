from rest_framework_simplejwt.tokens import RefreshToken # pyright: ignore[reportMissingImports]
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # pyright: ignore[reportMissingImports]
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from django.contrib.auth import get_user_model 
from ..serializers import UserSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to add user data to token claims"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['user_id'] = str(user.id)
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone'] = user.phone
        token['role'] = user.role
        token['is_verified'] = user.is_verified
        token['is_blocked'] = user.is_blocked
        token['is_admin'] = user.is_superuser or user.role == 'admin'
        token['full_name'] = f"{user.first_name} {user.last_name}".strip() or user.username
        
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class JWTService:
    """Service class for handling JWT token operations"""
    
    @staticmethod
    def create_tokens_for_user(user):
        """
        Create access and refresh tokens for a user with custom claims
        """
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'permissions': {
                'is_verified': user.is_verified,
                'is_blocked': user.is_blocked,
                'role': user.role,
                'is_admin': user.is_superuser or user.role == 'admin'
            }
        }
    
    @staticmethod
    def create_refresh_token(user):
        """Create only refresh token for user"""
        return CustomTokenObtainPairSerializer.get_token(user)
    
    @staticmethod
    def create_access_token(user):
        """Create only access token for user"""
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        return refresh.access_token
    
    @staticmethod
    def blacklist_token(token):
        """Blacklist a refresh token"""
        try:
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return True, "Token blacklisted successfully"
        except Exception as e:
            return False, f"Error blacklisting token: {str(e)}"
    
    @staticmethod
    def verify_token(token_string):
        """Verify if a token is valid"""
        try:
            token = RefreshToken(token_string)
            return True, "Token is valid"
        except Exception as e:
            return False, f"Invalid token: {str(e)}"
    
    @staticmethod
    def decode_token(token_string):
        """Decode token and return payload"""
        try:
            token = RefreshToken(token_string)
            return True, dict(token.payload)
        except Exception as e:
            return False, f"Error decoding token: {str(e)}"
    
    @staticmethod
    def get_user_from_token(token_string):
        """Get user object from token"""
        try:
            token = RefreshToken(token_string)
            user_id = token.payload.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                return True, user
            return False, "User ID not found in token"
        except User.DoesNotExist:
            return False, "User not found"
        except Exception as e:
            return False, f"Error getting user from token: {str(e)}"