from rest_framework import serializers
from ..models.player import Player


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def get_full_name(self, obj):
        return " ".join(
            part for part in [obj.first_name, obj.middle_names, obj.last_name] if part
        )
