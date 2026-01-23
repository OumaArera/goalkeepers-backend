from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated 
from ..models import User
from ..serializers import UserSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10              # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View to list users with pagination.
    Read-only for safety; no creation or update here.
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  
    pagination_class = StandardResultsSetPagination
