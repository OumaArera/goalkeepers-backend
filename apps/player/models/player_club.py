import uuid
from django.db import models
from ..models import *

class PlayerClub(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        "player.Player",
        on_delete=models.CASCADE,
        related_name="club_memberships"
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="players"
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    is_current = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["player"]),
            models.Index(fields=["club"]),
            models.Index(fields=["is_current"]),
            models.Index(fields=["player", "is_current"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["player", "club", "start_date"],
                name="unique_player_club_period"
            )
        ]

    def __str__(self):
        return f"{self.player} → {self.club}"
