from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Join
from ..serializers import JoinSerializer
from ..common import *


class JoinRequestListCreateAPIView(
    generics.ListCreateAPIView
):
    serializer_class = JoinSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Join.objects.filter(
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
                "count":
                self.paginator.page.paginator.count
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        join_request = serializer.save()

        return ApiResponse.success(
            data=JoinSerializer(
                join_request
            ).data,
            message="Request submitted successfully",
            status=status.HTTP_201_CREATED
        )
    
class JoinRequestRetrieveUpdateAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = JoinSerializer
    lookup_field = "id"

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return Join.objects.filter(
            is_active=True
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        return ApiResponse.success(
            data=JoinSerializer(
                instance
            ).data
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

        join_request = serializer.save()

        return ApiResponse.success(
            data=JoinSerializer(
                join_request
            ).data,
            message="Request updated successfully"
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.is_active = False

        instance.save(
            update_fields=["is_active"]
        )

        return ApiResponse.success(
            message="Request deleted successfully"
        )