from rest_framework import serializers
from ..models import Award


class AwardSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(
        source="player.__str__", read_only=True
    )

    class Meta:
        model = Award
        fields = "__all__"
        read_only_fields = [
            "id",
            "status",
            "created_by",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)


class AwardApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["status", "review_comment"]
