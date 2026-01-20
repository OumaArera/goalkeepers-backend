from rest_framework import serializers
from ..models import PlayerClub
from .club import *


class PlayerClubSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    club_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = PlayerClub
        fields = [
            "id",
            "player",
            "club",
            "club_id",
            "start_date",
            "end_date",
            "is_current",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        club_id = validated_data.pop("club_id")
        validated_data["club_id"] = club_id

        # Ensure only one current club
        if validated_data.get("is_current", False):
            PlayerClub.objects.filter(
                player=validated_data["player"],
                is_current=True
            ).update(is_current=False, end_date=validated_data["start_date"])

        return super().create(validated_data)
