from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Tag
from ..serializers import TagSerializer
from ..common import *


class TagListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
    ]

    ordering = ["name"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Tag.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={
                "count": self.paginator.page.paginator.count
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()

        return ApiResponse.success(
            data=TagSerializer(tag).data,
            message="Tag created successfully",
            status=status.HTTP_201_CREATED
        )


class TagRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TagSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Tag.objects.all()

    def retrieve(self, request, *args, **kwargs):
        tag = self.get_object()
        return ApiResponse.success(
            TagSerializer(tag).data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()



        return ApiResponse.success(
            TagSerializer(tag).data,
            message="Tag updated successfully"
        )