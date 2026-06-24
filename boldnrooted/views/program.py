from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Program
from ..serializers import ProgramSerializer
from ..filters import ProgramFilter
from ..common import *


class ProgramListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProgramSerializer
    pagination_class = StandardPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProgramFilter

    search_fields = ["title", "description", "location", "organizer"]
    ordering_fields = ["start_date", "end_date", "created_at"]
    ordering = ["-start_date"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Program.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        program = serializer.save()
        return ApiResponse.success(
            data=ProgramSerializer(program).data,
            message="Program created successfully",
            status=status.HTTP_201_CREATED
        )


class ProgramRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProgramSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Program.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        program = self.get_object()
        return ApiResponse.success(ProgramSerializer(program).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        program = serializer.save()
        return ApiResponse.success(
            ProgramSerializer(program).data,
            message="Program updated successfully"
        )