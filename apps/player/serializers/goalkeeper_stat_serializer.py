from rest_framework import serializers
from ..models import GoalkeeperStat


class GoalkeeperStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalkeeperStat
        fields = "__all__"
        read_only_fields = [
            "id",
            "status",
            "created_by",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        game = attrs.get("game")
        player = attrs.get("player")

        # Only validate on CREATE
        if self.instance is None:
            exists = GoalkeeperStat.objects.filter(
                game=game,
                player=player
            ).exists()

            if exists:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "Goalkeeper stats for this player and game already exist."
                        ]
                    }
                )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)
    
class GoalkeeperStatsApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalkeeperStat
        fields = ["status"]

