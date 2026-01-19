from rest_framework import serializers
from ..models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "home_team",
            "away_team",
            "match_date",
            "venue",
            "competition",
            "season",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
