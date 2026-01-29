from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import PlayerPlayStyle, Activity
from ..serializers import *
from ...common import *

class PlayerPlayStyleCreateAPIView(generics.CreateAPIView):
    serializer_class = PlayerPlayStyleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

        log_model_activity(
            self.request.user,
            Activity.Action.CREATED,
            serializer.instance
        )


class PlayerPlayStyleDeleteAPIView(generics.DestroyAPIView):
    queryset = PlayerPlayStyle.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        log_model_activity(
            self.request.user,
            Activity.Action.DELETED,
            instance
        )
        super().perform_destroy(instance)
