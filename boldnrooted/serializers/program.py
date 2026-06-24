from rest_framework import serializers
from ..models import Program


class ProgramSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "description",
            "organizer",
            "start_date",
            "end_date",
            "location",
            "poster",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]