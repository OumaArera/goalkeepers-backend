from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import PhysicalHealthAssessment
from ..serializers import *
from ..filters import PhysicalHealthAssessmentFilter
from ...common import ApiResponse, StandardPagination


class HealthAssessmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PhysicalHealthAssessmentSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_class = PhysicalHealthAssessmentFilter
    ordering_fields = ["assessment_date", "created_at"]
    ordering = ["-assessment_date"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PhysicalHealthAssessment.objects.select_related(
            "player", "game"
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assessment = serializer.save()

        return ApiResponse.success(
            data=self.get_serializer(assessment).data,
            message="Health assessment submitted successfully",
            status=status.HTTP_201_CREATED
        )


class HealthAssessmentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PhysicalHealthAssessmentSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return PhysicalHealthAssessment.objects.select_related(
            "player", "game"
        )

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
        assessment = serializer.save()

        return ApiResponse.success(
            data=self.get_serializer(assessment).data,
            message="Health assessment updated successfully"
        )


class HealthAssessmentApprovalAPIView(generics.UpdateAPIView):
    serializer_class = HealthAssessmentApprovalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    queryset = PhysicalHealthAssessment.objects.all()

    def update(self, request, *args, **kwargs):
        assessment = self.get_object()
        serializer = self.get_serializer(assessment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewed_by=request.user)

        return ApiResponse.success(
            data=serializer.data,
            message="Assessment status updated successfully"
        )
