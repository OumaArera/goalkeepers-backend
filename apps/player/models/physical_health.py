import uuid
from django.db import models
from django.conf import settings
from ..models import *


class PhysicalHealthAssessment(models.Model):
    class AssessmentType(models.TextChoices):
        PRE_MATCH = "PRE_MATCH", "Pre-Match"
        POST_MATCH = "POST_MATCH", "Post-Match"
        TRAINING = "TRAINING", "Training"
        MEDICAL = "MEDICAL", "Medical"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="health_assessments"
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="health_assessments",
        help_text="Optional: link assessment to a specific game"
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=AssessmentType.choices
    )

    assessment_date = models.DateField()

    # ─────────────────────────────
    # Core Physical Metrics (0–10)
    # ─────────────────────────────
    fitness_level = models.PositiveSmallIntegerField(help_text="Overall fitness (0–10)")
    fatigue_level = models.PositiveSmallIntegerField(help_text="Fatigue (0–10)")
    muscle_soreness = models.PositiveSmallIntegerField(help_text="Muscle soreness (0–10)")
    flexibility = models.PositiveSmallIntegerField(help_text="Flexibility (0–10)")
    mobility = models.PositiveSmallIntegerField(help_text="Mobility (0–10)")
    endurance = models.PositiveSmallIntegerField(help_text="Endurance (0–10)")

    # ─────────────────────────────
    # Injury & Recovery
    # ─────────────────────────────
    injury_risk = models.PositiveSmallIntegerField(help_text="Injury risk (0–10)")
    recovery_score = models.PositiveSmallIntegerField(help_text="Recovery quality (0–10)")
    pain_level = models.PositiveSmallIntegerField(help_text="Pain level (0–10)")

    # ─────────────────────────────
    # Computed / Analytical
    # ─────────────────────────────
    readiness_score = models.FloatField(
        default=0,
        help_text="Computed readiness score"
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

    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assessed_health_records"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_health_records"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-assessment_date"]
        indexes = [
            models.Index(fields=["player"]),
            models.Index(fields=["assessment_type"]),
            models.Index(fields=["assessment_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["player", "status"]),
        ]
        unique_together = ("player", "assessment_date", "assessment_type")

    def calculate_readiness_score(self):
        """
        Readiness Score Formula (0–10):
        Higher is better.
        """
        positive = (
            self.fitness_level +
            self.flexibility +
            self.mobility +
            self.endurance +
            self.recovery_score
        )
        negative = (
            self.fatigue_level +
            self.muscle_soreness +
            self.injury_risk +
            self.pain_level
        )
        score = (positive - negative) / 5
        return round(max(0, min(score, 10)), 2)

    def save(self, *args, **kwargs):
        self.readiness_score = self.calculate_readiness_score()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player} - {self.assessment_date}"
