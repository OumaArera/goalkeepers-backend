import uuid
from django.db import models
from django.conf import settings
from apps.player.models import Player
from ..models import Game


class TrainingLoad(models.Model):
    class SessionType(models.TextChoices):
        TRAINING = "TRAINING", "Training"
        MATCH = "MATCH", "Match"
        RECOVERY = "RECOVERY", "Recovery"
        GYM = "GYM", "Gym"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="training_loads"
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_loads"
    )

    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices
    )

    session_date = models.DateField()

    duration_minutes = models.PositiveIntegerField(
        help_text="Total session duration in minutes"
    )

    # ─────────────────────────────
    # GPS & Load Metrics
    # ─────────────────────────────
    total_distance_km = models.FloatField(default=0)
    high_speed_distance_km = models.FloatField(default=0)
    sprint_distance_km = models.FloatField(default=0)

    sprint_count = models.PositiveIntegerField(default=0)
    accelerations = models.PositiveIntegerField(default=0)
    decelerations = models.PositiveIntegerField(default=0)

    max_speed_kmh = models.FloatField(default=0)

    # ─────────────────────────────
    # Physiological (Optional)
    # ─────────────────────────────
    avg_heart_rate = models.PositiveIntegerField(null=True, blank=True)
    max_heart_rate = models.PositiveIntegerField(null=True, blank=True)

    # ─────────────────────────────
    # Computed Load Scores
    # ─────────────────────────────
    player_load = models.FloatField(
        default=0,
        help_text="Overall workload score"
    )

    intensity_score = models.FloatField(
        default=0,
        help_text="Load per minute"
    )

    notes = models.TextField(blank=True)

    # ─────────────────────────────
    # Workflow
    # ─────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recorded_training_loads"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_training_loads"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-session_date"]
        indexes = [
            models.Index(fields=["player"]),
            models.Index(fields=["session_date"]),
            models.Index(fields=["session_type"]),
            models.Index(fields=["status"]),
        ]
        unique_together = ("player", "session_date", "session_type")

    def calculate_player_load(self):
        """
        Simplified Player Load formula
        """
        return round(
            (
                self.total_distance_km * 10 +
                self.high_speed_distance_km * 20 +
                self.sprint_count * 2 +
                self.accelerations +
                self.decelerations
            ),
            2
        )

    def calculate_intensity(self):
        if self.duration_minutes == 0:
            return 0
        return round(self.player_load / self.duration_minutes, 2)

    def save(self, *args, **kwargs):
        self.player_load = self.calculate_player_load()
        self.intensity_score = self.calculate_intensity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player} - {self.session_date} ({self.session_type})"
