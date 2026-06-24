from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from ..models import User
from ..serializers import UserSerializer
from ...common import *

class UserViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Users:
    - List (with pagination)
    - Retrieve single user by ID
    - Update user
    - Delete user
    """
    queryset = User.objects.exclude(role="bold").order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 
    pagination_class = StandardPagination

    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "email", "phone", "role"]

    # Optional: restrict destructive actions to admins
    def destroy(self, request, *args, **kwargs):
        
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Partial update allowed by default (PATCH), full update (PUT) supported.
        """
        return super().update(request, *args, **kwargs)
