from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import *
from ..serializers import *
from ..filters import TrainingLoadFilter
from ...common import *


class TrainingLoadListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TrainingLoadSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_class = TrainingLoadFilter
    ordering_fields = ["session_date", "player_load", "intensity_score"]
    ordering = ["-session_date"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return TrainingLoad.objects.select_related("player", "game")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        load = serializer.save()
        log_model_activity(request.user, Activity.Action.CREATED, load)
        return ApiResponse.success(
            data=self.get_serializer(load).data,
            message="Training load recorded successfully",
            status=status.HTTP_201_CREATED
        )


class TrainingLoadRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TrainingLoadSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return TrainingLoad.objects.select_related("player", "game")

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
        load = serializer.save()

        return ApiResponse.success(
            data=self.get_serializer(load).data,
            message="Training load updated successfully"
        )


class TrainingLoadApprovalAPIView(generics.UpdateAPIView):
    serializer_class = TrainingLoadApprovalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    queryset = TrainingLoad.objects.all()

    def update(self, request, *args, **kwargs):
        load = self.get_object()
        serializer = self.get_serializer(load, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewed_by=request.user)
        log_model_activity(request.user, Activity.Action.UPDATED, load)
        return ApiResponse.success(
            data=serializer.data,
            message="Training load status updated successfully"
        )
