import uuid
from django.db import models


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to="clubs/logos/", null=True, blank=True)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)

    founded_year = models.PositiveIntegerField(null=True, blank=True)
    stadium_name = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["country"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name
