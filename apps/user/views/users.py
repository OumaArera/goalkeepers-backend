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

    # Optional: restrict destructive actions to admins
    def destroy(self, request, *args, **kwargs):
        # if not request.user.is_superuser:
        #     return Response(
        #         {"detail": "You do not have permission to delete this user."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Partial update allowed by default (PATCH), full update (PUT) supported.
        """
        return super().update(request, *args, **kwargs)
