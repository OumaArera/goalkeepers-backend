from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import PrayerRequest
from ..serializers import PrayerRequestSerializer
from ..common import *

class PrayerRequestListCreateAPIView(
    generics.ListCreateAPIView
):
    serializer_class = PrayerRequestSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PrayerRequest.objects.filter(
            is_active=True
        )

    def list(self, request, *args, **kwargs):
        response = super().list(
            request,
            *args,
            **kwargs
        )

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

        prayer = serializer.save()

        return ApiResponse.success(
            data=PrayerRequestSerializer(prayer).data,
            message="Prayer request submitted successfully",
            status=status.HTTP_201_CREATED
        )
    
class PrayerRequestRetrieveUpdateAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PrayerRequestSerializer
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
        return PrayerRequest.objects.filter(
            is_active=True
        )

    def retrieve(self, request, *args, **kwargs):
        prayer = self.get_object()

        return ApiResponse.success(
            data=PrayerRequestSerializer(prayer).data
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

        prayer = serializer.save()

        return ApiResponse.success(
            data=PrayerRequestSerializer(prayer).data,
            message="Prayer request updated successfully"
        )

    def destroy(self, request, *args, **kwargs):
        prayer = self.get_object()

        prayer.is_active = False
        prayer.save(
            update_fields=["is_active"]
        )

        return ApiResponse.success(
            message="Prayer request deleted successfully"
        )
    
class PrayForRequestAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, id):
        prayer = get_object_or_404(
            PrayerRequest,
            id=id,
            is_active=True
        )

        prayer.prayed_count += 1

        prayer.save(
            update_fields=["prayed_count"]
        )

        return ApiResponse.success(
            data={
                "id": str(prayer.id),
                "prayed_count": prayer.prayed_count
            },
            message="Prayer recorded successfully"
        )