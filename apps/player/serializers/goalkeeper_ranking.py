from rest_framework import serializers
from ..models import Player


class GoalkeeperRankingSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    matches_played = serializers.IntegerField(read_only=True)
    avg_saves = serializers.FloatField(read_only=True)
    clean_sheets = serializers.IntegerField(read_only=True)
    goals_conceded = serializers.IntegerField(read_only=True)
    ranking_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "full_name",
            "avatar",
            "matches_played",
            "avg_saves",
            "clean_sheets",
            "goals_conceded",
            "ranking_score",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
