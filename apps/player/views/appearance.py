from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..serializers import *
from ...common import *

class PlayerAppearanceCreateAPIView(generics.CreateAPIView):
    serializer_class = PlayerAppearanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        appearance = serializer.save(
            created_by=self.request.user
        )

        log_model_activity(
            self.request.user,
            Activity.Action.CREATED,
            appearance
        )


class PlayerAppearanceListAPIView(generics.ListAPIView):
    serializer_class = PlayerAppearanceSerializer

    def get_queryset(self):
        return PlayerAppearance.objects.filter(
            player_id=self.kwargs["player_id"]
        )


class PlayerAppearanceRetrieveUpdateAPIView(
    generics.RetrieveUpdateAPIView
):
    queryset = PlayerAppearance.objects.select_related("player")
    serializer_class = PlayerAppearanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        appearance = serializer.save()

        log_model_activity(
            self.request.user,
            Activity.Action.UPDATED,
            appearance
        )


class PlayerAppearanceDeleteAPIView(generics.DestroyAPIView):
    queryset = PlayerAppearance.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        log_model_activity(
            self.request.user,
            Activity.Action.DELETED,
            instance
        )
        super().perform_destroy(instance)
