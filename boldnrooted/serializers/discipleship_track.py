from rest_framework import serializers
from ..models import (
    DiscipleshipTrack,
    DiscipleshipModule
)

class DiscipleshipModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscipleshipModule
        fields = "__all__"


class DiscipleshipTrackSerializer(serializers.ModelSerializer):
    modules = DiscipleshipModuleSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DiscipleshipTrack
        fields = "__all__"