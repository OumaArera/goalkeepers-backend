from rest_framework import serializers

from ..serializers.blog import TagSerializer
from ..models import Event

class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )

    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Event

        fields = [
            "id",
            "slug",
            "title",
            "event_type",
            "event_date",
            "start_time",
            "end_time",
            "location",
            "format",
            "capacity",
            "description",
            "speakers",
            "gradient",
            "accent_gradient",
            "accent",
            "featured",
            "registration_open",
            "banner",
            "tags",
            "tag_ids",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tag_ids = validated_data.pop(
            "tag_ids",
            []
        )

        event = Event.objects.create(
            **validated_data
        )

        event.tags.set(tag_ids)

        return event

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop(
            "tag_ids",
            None
        )

        event = super().update(
            instance,
            validated_data
        )

        if tag_ids is not None:
            event.tags.set(tag_ids)

        return event