import uuid
from django.db import models
from .player import Player


class PlayerPlayStyle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="play_styles"
    )

    label = models.CharField(
        max_length=100,
        help_text="Player-defined style description"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("player", "label")

    def __str__(self):
        return self.label
