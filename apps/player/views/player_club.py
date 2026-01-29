from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import *
from ..serializers import PlayerClubSerializer
from ...common import *


class PlayerClubCreateAPIView(generics.CreateAPIView):
    serializer_class = PlayerClubSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        player_club = serializer.save()

        log_model_activity(
            user=self.request.user,
            action=Activity.Action.CREATED,
            instance=player_club
        )


class PlayerClubListAPIView(generics.ListAPIView):
    serializer_class = PlayerClubSerializer

    def get_queryset(self):
        player_id = self.kwargs["player_id"]
        return (
            PlayerClub.objects
            .filter(player_id=player_id)
            .select_related("club", "player")
        )


class PlayerClubRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = PlayerClub.objects.select_related("player", "club")
    serializer_class = PlayerClubSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        player_club = serializer.save()

        log_model_activity(
            user=self.request.user,
            action=Activity.Action.UPDATED,
            instance=player_club
        )



