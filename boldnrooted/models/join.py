import uuid
from django.db import models


class Join(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    country = models.CharField(
        max_length=100
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    how_heard_about_us = models.CharField(
        max_length=255,
        blank=True
    )

    about = models.TextField(
        blank=True
    )

    contacted = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"