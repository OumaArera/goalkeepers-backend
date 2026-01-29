from rest_framework import serializers
from ..models import Club


class ClubMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "short_name",
            "logo",
        ]
