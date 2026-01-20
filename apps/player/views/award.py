from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Award
from ..serializers import *
from ..filters import AwardFilter
from ...common import ApiResponse, StandardPagination


class AwardListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AwardSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = AwardFilter
    search_fields = ["title", "competition", "season"]
    ordering_fields = ["award_date", "created_at"]
    ordering = ["-award_date"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Award.objects.select_related("player")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        award = serializer.save()

        return ApiResponse.success(
            data=AwardSerializer(award).data,
            message="Award submitted successfully",
            status=status.HTTP_201_CREATED
        )


class AwardRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AwardSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Award.objects.select_related("player")

    def retrieve(self, request, *args, **kwargs):
        return ApiResponse.success(
            self.get_serializer(self.get_object()).data
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        award = serializer.save()

        return ApiResponse.success(
            data=self.get_serializer(award).data,
            message="Award updated successfully"
        )


class AwardApprovalAPIView(generics.UpdateAPIView):
    serializer_class = AwardApprovalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    queryset = Award.objects.all()

    def update(self, request, *args, **kwargs):
        award = self.get_object()
        serializer = self.get_serializer(award, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewed_by=request.user)

        return ApiResponse.success(
            data=serializer.data,
            message="Award status updated successfully"
        )
