from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid


class Activity(models.Model):
    class Action(models.TextChoices):
        CREATED = "CREATED", "Created"
        UPDATED = "UPDATED", "Updated"
        DELETED = "DELETED", "Deleted"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"
        VIEWED = "VIEWED", "Viewed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities"
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices
    )

    # Generic reference to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable summary"
    )

    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional contextual data"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user} {self.action} {self.content_type}"
