from rest_framework import serializers
from .club import ClubSerializer
from .award import AwardSerializer
from .play_style import PlayerPlayStyleSerializer
from .appearance import PlayerAppearanceSerializer
from ..models import Player


class PlayerDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    clubs = serializers.SerializerMethodField()
    play_styles = PlayerPlayStyleSerializer(many=True, read_only=True)
    appearances = PlayerAppearanceSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "full_name",
            "avatar",
            "first_name",
            "middle_names",
            "last_name",
            "date_of_birth",
            "height",
            "weight",
            "sex",
            "preferred_foot",
            "injured",
            "country_of_birth",
            "country_of_residence",
            "clubs",
            "awards",
            "play_styles",
            "appearances",
        ]

    def get_full_name(self, obj):
        return " ".join(
            p for p in [obj.first_name, obj.middle_names, obj.last_name] if p
        )

    def get_clubs(self, obj):
        request = self.context.get("request")
        return ClubSerializer(
            [m.club for m in obj.club_memberships.all()],
            many=True,
            context={"request": request}
        ).data
