from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ScriptureReference
from ..serializers import ScriptureReferenceSerializer
from ..common import *


class ScriptureReferenceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ScriptureReferenceSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "book",
    ]

    ordering_fields = [
        "book",
        "chapter",
        "verse_start",
    ]

    ordering = ["book", "chapter", "verse_start"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return ScriptureReference.objects.all()

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
        scripture = serializer.save()



        return ApiResponse.success(
            data=ScriptureReferenceSerializer(scripture).data,
            message="Scripture reference created successfully",
            status=status.HTTP_201_CREATED
        )


class ScriptureReferenceRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ScriptureReferenceSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return ScriptureReference.objects.all()

    def retrieve(self, request, *args, **kwargs):
        scripture = self.get_object()
        return ApiResponse.success(
            ScriptureReferenceSerializer(scripture).data
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
        scripture = serializer.save()



        return ApiResponse.success(
            ScriptureReferenceSerializer(scripture).data,
            message="Scripture reference updated successfully"
        )