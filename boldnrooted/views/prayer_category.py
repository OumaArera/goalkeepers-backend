from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import PrayerCategory
from ..serializers import PrayerCategorySerializer
from ..common import *

class PrayerCategoryListCreateAPIView(
    generics.ListCreateAPIView
):
    serializer_class = PrayerCategorySerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PrayerCategory.objects.filter(
            is_active=True
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return ApiResponse.success(
            data=response.data,
            meta={
                "count": self.paginator.page.paginator.count
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = serializer.save()

        return ApiResponse.success(
            data=PrayerCategorySerializer(category).data,
            message="Prayer category created successfully",
            status=status.HTTP_201_CREATED
        )
    
class PrayerCategoryRetrieveUpdateAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PrayerCategorySerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in [
            "PUT",
            "PATCH",
            "DELETE"
        ]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PrayerCategory.objects.filter(
            is_active=True
        )

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()

        return ApiResponse.success(
            data=PrayerCategorySerializer(category).data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = serializer.save()

        return ApiResponse.success(
            data=PrayerCategorySerializer(category).data,
            message="Prayer category updated successfully"
        )

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        category.is_active = False
        category.save(
            update_fields=["is_active"]
        )

        return ApiResponse.success(
            message="Prayer category deleted successfully"
        )