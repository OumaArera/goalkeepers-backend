from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import *
from ..serializers import GameSerializer
from ..filters import GameFilter
from ...common import *


class GameListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = GameFilter
    search_fields = [
        "home_team",
        "away_team",
        "competition",
        "season",
    ]
    ordering_fields = [
        "match_date",
        "created_at",
        "home_team",
        "away_team",
    ]
    ordering = ["-match_date"]

    def get_permissions(self):
        """
        Public access for GET,
        Authentication required for POST
        """
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Game.objects.filter(is_active=True)

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
        game = serializer.save()
        log_model_activity(request.user, Activity.Action.CREATED, game)
        return ApiResponse.success(
            data=GameSerializer(game).data,
            message="Game created successfully",
            status=status.HTTP_201_CREATED
        )


class GameRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = GameSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Game.objects.all()

    def retrieve(self, request, *args, **kwargs):
        game = self.get_object()
        return ApiResponse.success(GameSerializer(game).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        game = serializer.save()
        log_model_activity(request.user, Activity.Action.UPDATED, game)
        return ApiResponse.success(
            GameSerializer(game).data,
            message="Game updated successfully"
        )
