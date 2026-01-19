import uuid
from django.db import models


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)

    match_date = models.DateField()
    venue = models.CharField(max_length=255, blank=True)

    competition = models.CharField(
        max_length=255,
        blank=True,
        help_text="League, tournament or competition name"
    )

    season = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: 2024/2025"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Soft toggle to hide deprecated games"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-match_date"]
        indexes = [
            models.Index(fields=["match_date"]),
            models.Index(fields=["home_team"]),
            models.Index(fields=["away_team"]),
            models.Index(fields=["competition"]),
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
