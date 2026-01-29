import uuid
from django.db import models
from django.conf import settings
from ..models import Game, Player


class GoalkeeperStat(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="goalkeeper_stats"
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="goalkeeper_stats"
    )

    # ─────────────────────────────
    # Shot Stopping
    # ─────────────────────────────
    saves = models.PositiveIntegerField(default=0)
    penalty_saved = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Aerial & Ball Handling
    # ─────────────────────────────
    catches = models.PositiveIntegerField(default=0)
    punches = models.PositiveIntegerField(default=0)
    high_claims = models.PositiveIntegerField(default=0)
    build_up = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Distribution
    # ─────────────────────────────
    throw_outs = models.PositiveIntegerField(default=0)
    goal_kicks = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Defensive Stats
    # ─────────────────────────────
    sweeper_clearances = models.PositiveIntegerField(default=0)
    clean_sheet = models.BooleanField(default=False)
    goals_conceded = models.PositiveIntegerField(default=0)
    error_leading_to_goal = models.PositiveIntegerField(default=0)
    own_goals = models.PositiveIntegerField(default=0)
    total_missed_passes = models.PositiveIntegerField(default=0)
    inaccurate_long_balls = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Goals Conceded by Type
    # ─────────────────────────────
    corner_goals_conceded = models.PositiveIntegerField(default=0)
    penalty_goals_conceded = models.PositiveIntegerField(default=0)
    free_kick_goals_conceded = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Team Player Stats
    # ─────────────────────────────
    total_passes = models.PositiveIntegerField(default=0)
    passes_per_match = models.FloatField(default=0)
    accurate_long_balls = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)

    # ─────────────────────────────
    # Workflow
    # ─────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_goalkeeper_stats"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_goalkeeper_stats"
    )

    review_comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("game", "player")
        indexes = [
            models.Index(fields=["game"]),
            models.Index(fields=["player"]),
            models.Index(fields=["status"]),
            models.Index(fields=["player", "status"]),
            models.Index(fields=["player", "status", "game"]),
        ]

    def __str__(self):
        return f"{self.player} - {self.game}"
