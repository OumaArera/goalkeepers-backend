from rest_framework import serializers
from django.utils import timezone
from ..models import *


class ScriptureReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptureReference
        fields = "__all__"




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"




class BlogPostSerializer(serializers.ModelSerializer):
    scripture_references = ScriptureReferenceSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    scripture_reference_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "content",
            "scripture_references",
            "scripture_reference_ids",
            "tags",
            "tag_ids",
            "is_published",
            "published_at",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "author",
            "published_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        scripture_ids = validated_data.pop("scripture_reference_ids", [])
        tag_ids = validated_data.pop("tag_ids", [])

        validated_data["author"] = self.context["request"].user

        if validated_data.get("is_published"):
            validated_data["published_at"] = timezone.now()

        blog = super().create(validated_data)

        blog.scripture_references.set(scripture_ids)
        blog.tags.set(tag_ids)

        return blog

    def update(self, instance, validated_data):
        scripture_ids = validated_data.pop("scripture_reference_ids", None)
        tag_ids = validated_data.pop("tag_ids", None)

        if validated_data.get("is_published") and not instance.published_at:
            validated_data["published_at"] = timezone.now()

        blog = super().update(instance, validated_data)

        if scripture_ids is not None:
            blog.scripture_references.set(scripture_ids)

        if tag_ids is not None:
            blog.tags.set(tag_ids)

        return blog