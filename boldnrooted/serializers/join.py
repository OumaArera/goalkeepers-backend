from rest_framework import serializers
from ..models import Join


class JoinSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Join

        fields = "__all__"

        read_only_fields = [
            "id",
            "contacted",
            "created_at",
            "updated_at",
        ]