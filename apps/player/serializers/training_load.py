from rest_framework import serializers
from ..models import TrainingLoad


class TrainingLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingLoad
        fields = "__all__"
        read_only_fields = [
            "id",
            "player_load",
            "intensity_score",
            "status",
            "recorded_by",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["recorded_by"] = self.context["request"].user
        return super().create(validated_data)


class TrainingLoadApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingLoad
        fields = ["status"]
