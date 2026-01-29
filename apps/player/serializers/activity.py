from rest_framework import serializers
from ..models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    object_type = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "action",
            "description",
            "object_type",
            "object_id",
            "created_at",
        ]

    def get_object_type(self, obj):
        return obj.content_type.model
