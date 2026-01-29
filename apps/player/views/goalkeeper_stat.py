from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import *
from ..serializers import *
from ..filters import GoalkeeperStatFilter
from ...common import *
from django.db import IntegrityError


class GoalkeeperStatsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GoalkeeperStatSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = GoalkeeperStatFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return GoalkeeperStat.objects.select_related(
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

        try:
            stats = serializer.save()
            log_model_activity(request.user, Activity.Action.CREATED, stats)
        except IntegrityError:
            return ApiResponse.error(
                message="Goalkeeper stats for this player and game already exist.",
                status=status.HTTP_400_BAD_REQUEST
            )

        return ApiResponse.success(
            data=GoalkeeperStatSerializer(stats).data,
            message="Goalkeeper stats submitted successfully",
            status=status.HTTP_201_CREATED
        )


class GoalkeeperStatsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = GoalkeeperStatFilter
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return GoalkeeperStat.objects.select_related(
            "player", "game"
        )

    def retrieve(self, request, *args, **kwargs):
        return ApiResponse.success(self.get_serializer(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        stats = serializer.save()
        log_model_activity(request.user, Activity.Action.UPDATED, stats)
        return ApiResponse.success(
            data=self.get_serializer(stats).data,
            message="Stats updated successfully"
        )


class GoalkeeperStatsApprovalAPIView(generics.UpdateAPIView):
    serializer_class = GoalkeeperStatsApprovalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    queryset = GoalkeeperStat.objects.all()

    def update(self, request, *args, **kwargs):
        stats = self.get_object()
        serializer = self.get_serializer(stats, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ApiResponse.success(
            data=serializer.data,
            message="Stats status updated successfully"
        )

