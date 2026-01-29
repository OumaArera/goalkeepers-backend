from rest_framework import serializers
from ..models import PlayerAppearance


class PlayerAppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAppearance
        fields = [
            "id",
            "player",
            "competition",
            "season",
            "description",
            "recognitions",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_competition(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "Competition name is too short."
            )
        return value

    def validate_recognitions(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Recognitions must be a list."
            )

        for item in value:
            if not isinstance(item, str):
                raise serializers.ValidationError(
                    "Each recognition must be a string."
                )

        return value
