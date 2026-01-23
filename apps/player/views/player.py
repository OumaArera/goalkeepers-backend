from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated

# from apps.player.serializers.player import PlayerListSerializer

from ..querysets import player_detail_analytics, player_list_queryset
from ..models import Player
from ..serializers import *
from ..filters import PlayerFilter
from ...common import *


class PlayerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PlayerFilter
    search_fields = [
        "first_name",
        "middle_names",
        "last_name",
        "phone",
        "email",
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "date_of_birth",
        "height",
        "created_at",
    ]
    ordering = ["last_name"]

    def get_permissions(self):
        """
        Public access for GET,
        Authentication required for POST
        """
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PlayerListSerializer
        return PlayerSerializer

    def get_queryset(self):
        return player_list_queryset()

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
        player = serializer.save()
        return ApiResponse.success(
            data=PlayerSerializer(
                player,
                context={"request": request}
            ).data,
            message="Player created successfully",
            status=status.HTTP_201_CREATED
        )



class PlayerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PlayerSerializer
    lookup_field = "id"

    def get_permissions(self):
        """
        Public access for GET,
        Authentication required for PUT/PATCH
        """
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Player.objects.select_related("user")

    def retrieve(self, request, *args, **kwargs):
        player = (
            Player.objects
            .select_related("user")
            .prefetch_related(
                "club_memberships__club",
                "awards"
            )
            .get(id=kwargs["id"])
        )

        year = request.query_params.get("year")
        serializer_context = {"request": request}

        return ApiResponse.success(
            data={
                "player": PlayerSerializer(
                    player,
                    context=serializer_context
                ).data,
                "analytics": player_detail_analytics(player, year),
                "clubs": ClubSerializer(
                    [m.club for m in player.club_memberships.all()],
                    many=True,
                    context=serializer_context
                ).data,
                "awards": AwardSerializer(
                    player.awards.all(),
                    many=True,
                    context=serializer_context
                ).data,
            }
        )


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        player = serializer.save()

        return ApiResponse.success(
            PlayerSerializer(player).data,
            message="Player updated successfully"
        )
