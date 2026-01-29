from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Activity
from ..serializers import ActivitySerializer
from ...common import *


class MyActivityListAPIView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return (
            Activity.objects
            .filter(user=self.request.user)
            .select_related("content_type")
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={
                "count": self.paginator.page.paginator.count
            }
        )
