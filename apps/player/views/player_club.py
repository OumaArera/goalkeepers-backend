from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import PlayerClub
from ..serializers import PlayerClubSerializer


class PlayerClubCreateAPIView(generics.CreateAPIView):
    serializer_class = PlayerClubSerializer
    permission_classes = [IsAuthenticated]


class PlayerClubListAPIView(generics.ListAPIView):
    serializer_class = PlayerClubSerializer

    def get_queryset(self):
        player_id = self.kwargs["player_id"]
        return (
            PlayerClub.objects
            .filter(player_id=player_id)
            .select_related("club", "player")
        )
