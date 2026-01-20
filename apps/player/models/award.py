import uuid
from django.db import models
from django.conf import settings
from ..models import Player


class Award(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="awards"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    competition = models.CharField(
        max_length=255,
        blank=True,
        help_text="League, tournament, or organization"
    )

    season = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g. 2024/2025"
    )

    award_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_awards"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_awards"
    )

    review_comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-award_date"]
        indexes = [
            models.Index(fields=["player"]),
            models.Index(fields=["status"]),
            models.Index(fields=["award_date"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.player}"
