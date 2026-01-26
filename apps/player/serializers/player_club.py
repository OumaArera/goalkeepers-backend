from rest_framework import serializers
from ..models import PlayerClub
from .club import ClubSerializer


class PlayerClubSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    club_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = PlayerClub
        fields = [
            "id",
            "player",
            "club",
            "club_id",
            "start_date",
            "end_date",
            "is_current",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        club_id = validated_data.pop("club_id")
        validated_data["club_id"] = club_id

        self._handle_current_club(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle club change (optional)
        club_id = validated_data.pop("club_id", None)
        if club_id:
            validated_data["club_id"] = club_id

        self._handle_current_club(validated_data, instance)

        return super().update(instance, validated_data)

    def _handle_current_club(self, validated_data, instance=None):
        """
        Ensures a player has only one current club.
        Works for both create and update.
        """
        is_current = validated_data.get(
            "is_current",
            instance.is_current if instance else False
        )

        if is_current:
            player = validated_data.get(
                "player",
                instance.player if instance else None
            )

            start_date = validated_data.get(
                "start_date",
                instance.start_date if instance else None
            )

            qs = PlayerClub.objects.filter(
                player=player,
                is_current=True
            )

            if instance:
                qs = qs.exclude(id=instance.id)

            qs.update(
                is_current=False,
                end_date=start_date
            )
