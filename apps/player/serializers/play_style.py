from rest_framework import serializers
from ..models import PlayerPlayStyle


class PlayerPlayStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPlayStyle
        fields = ["id", "label", "player"]
        read_only_fields = ["id"]

    def validate_label(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Play style description is too short."
            )

        if len(value) > 100:
            raise serializers.ValidationError(
                "Play style description is too long."
            )

        return value

    
