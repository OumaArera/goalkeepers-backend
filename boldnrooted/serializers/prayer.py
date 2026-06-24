from rest_framework import serializers
from ..models import PrayerCategory, PrayerRequest

class PrayerCategorySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PrayerCategory
        fields = "__all__"

class PrayerRequestSerializer(
    serializers.ModelSerializer
):
    category = PrayerCategorySerializer(
        read_only=True
    )

    category_id = serializers.UUIDField(
        write_only=True
    )

    class Meta:
        model = PrayerRequest

        fields = [
            "id",
            "name",
            "location",
            "category",
            "category_id",
            "text",
            "anonymous",
            "answered",
            "prayed_count",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "prayed_count",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        category_id = validated_data.pop(
            "category_id"
        )

        return PrayerRequest.objects.create(
            category_id=category_id,
            **validated_data
        )

    def update(self, instance, validated_data):
        category_id = validated_data.pop(
            "category_id",
            None
        )

        if category_id:
            instance.category_id = category_id

        return super().update(
            instance,
            validated_data
        )