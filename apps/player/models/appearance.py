import uuid
from django.conf import settings
from django.db import models



class PlayerAppearance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        "player.Player",
        on_delete=models.CASCADE,
        related_name="appearances"
    )

    competition = models.CharField(
        max_length=150,
        help_text="Competition or tournament name e.g. AFCON 2025"
    )

    season = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional season or year context"
    )

    description = models.TextField(
        blank=True,
        help_text="Optional context or notes"
    )

    recognitions = models.JSONField(
        default=list,
        blank=True,
        help_text="List of trophies, awards, or recognitions"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_appearances"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["competition"]),
        ]

    def __str__(self):
        return f"{self.player} – {self.competition}"
