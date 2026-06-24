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
    play_styles = serializers.SerializerMethodField()
    appearances = serializers.SerializerMethodField()
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
            "weight",
            "sex",
            "injured",
            "preferred_foot",
            "country_of_birth",
            "country_of_residence",
            "goalkeeper_averages",
            "clubs",
            "awards",
            "play_styles",
            "appearances",
            "is_active"
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

    def get_play_styles(self, obj):
        return [ps.label for ps in obj.play_styles.all()]

    
    def get_appearances(self, obj):
        return [
            {
                "competition": a.competition,
                "season": a.season,
                "recognitions": a.recognitions,
            }
            for a in obj.appearances.all()
        ]



