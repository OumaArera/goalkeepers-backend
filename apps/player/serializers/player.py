from rest_framework import serializers

from .award import AwardSerializer
from ..models import Player
from .club import ClubSerializer


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def get_full_name(self, obj):
        return " ".join(
            part for part in [obj.first_name, obj.middle_names, obj.last_name] if part
        )


class PlayerListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    goalkeeper_averages = serializers.SerializerMethodField()

    clubs = serializers.SerializerMethodField()
    awards = AwardSerializer(many=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "full_name",
            "avatar",
            "date_of_birth",
            "height",
            "country_of_birth",
            "country_of_residence",
            "goalkeeper_averages",
            "clubs",
            "awards",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_clubs(self, obj):
        request = self.context.get("request")
        return ClubSerializer(
            [m.club for m in obj.club_memberships.all()],
            many=True,
            context={"request": request}
        ).data

    def get_goalkeeper_averages(self, obj):
        return {
            key.replace("avg_", ""): getattr(obj, key)
            for key in obj.__dict__
            if key.startswith("avg_")
        } | {
            "clean_sheet_rate": obj.clean_sheet_rate
        }


