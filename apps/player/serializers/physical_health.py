from rest_framework import serializers
from ..models import PhysicalHealthAssessment
from .keeper_stats import GoalkeeperStatPlayerSerializer
from ...user.serializers import UserSerializer


class PhysicalHealthAssessmentSerializer(serializers.ModelSerializer):
    player = GoalkeeperStatPlayerSerializer(read_only=True)
    assessed_by = UserSerializer(read_only=True)
    class Meta:
        model = PhysicalHealthAssessment
        fields = "__all__"
        read_only_fields = [
            "id",
            "readiness_score",
            "status",
            "assessed_by",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["assessed_by"] = self.context["request"].user
        return super().create(validated_data)


class HealthAssessmentApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalHealthAssessment
        fields = ["status"]
