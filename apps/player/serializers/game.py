from rest_framework import serializers
from ..models import Game
from .club_minimal import ClubMinimalSerializer


class GameSerializer(serializers.ModelSerializer):
    home_team = ClubMinimalSerializer(read_only=True)
    away_team = ClubMinimalSerializer(read_only=True)

    home_team_id = serializers.UUIDField(write_only=True)
    away_team_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "home_team",
            "away_team",
            "home_team_id",
            "away_team_id",
            "match_date",
            "venue",
            "competition",
            "season",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        home_team_id = validated_data.pop("home_team_id")
        away_team_id = validated_data.pop("away_team_id")

        validated_data["home_team_id"] = home_team_id
        validated_data["away_team_id"] = away_team_id

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "home_team_id" in validated_data:
            instance.home_team_id = validated_data.pop("home_team_id")

        if "away_team_id" in validated_data:
            instance.away_team_id = validated_data.pop("away_team_id")

        return super().update(instance, validated_data)
