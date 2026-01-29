import uuid
from django.db import models
from .club import Club


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    home_team = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name="home_games"
    )

    away_team = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name="away_games"
    )

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
            models.Index(fields=["competition"]),
            models.Index(fields=["season"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["home_team", "away_team", "match_date"],
                name="unique_match_per_day"
            ),
            models.CheckConstraint(
                check=~models.Q(home_team=models.F("away_team")),
                name="home_and_away_must_differ"
            ),
        ]

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"
