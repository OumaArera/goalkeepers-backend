from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Club, Activity
from ..serializers import ClubSerializer
from ..filters import ClubFilter
from ...common import *


class ClubListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ClubSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ClubFilter
    search_fields = ["name", "short_name", "city", "country"]
    ordering_fields = ["name", "country", "created_at"]
    ordering = ["name"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Club.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = serializer.save()
        log_model_activity(request.user, Activity.Action.CREATED, club)
        return ApiResponse.success(
            data=ClubSerializer(club).data,
            message="Club created successfully",
            status=status.HTTP_201_CREATED
        )


class ClubRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ClubSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Club.objects.all()

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
        club = serializer.save()
        log_model_activity(request.user, Activity.Action.UPDATED, club)
        return ApiResponse.success(
            data=ClubSerializer(club).data,
            message="Club updated successfully"
        )
