from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # adjust as needed
    pagination_class = StandardPagination
    search_fields = ["first_name", "last_name", "email", "phone", "role"]

    # Optional: restrict destructive actions to admins
    def destroy(self, request, *args, **kwargs):
        
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Partial update allowed by default (PATCH), full update (PUT) supported.
        """
        return super().update(request, *args, **kwargs)
