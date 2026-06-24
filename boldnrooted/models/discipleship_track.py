import uuid
from django.db import models


class DiscipleshipTrack(models.Model):
    LEVEL_CHOICES = (
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    level = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES
    )

    weeks = models.PositiveIntegerField()

    gradient = models.CharField(max_length=255)
    accent = models.CharField(max_length=20)

    icon = models.CharField(max_length=20)

    description = models.TextField()

    verse = models.TextField()
    verse_reference = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["weeks"]

    def __str__(self):
        return self.title
    

class DiscipleshipModule(models.Model):
    MODULE_TYPES = (
        ("reading", "Reading"),
        ("teaching", "Teaching"),
        ("practice", "Practice"),
        ("special", "Special"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    track = models.ForeignKey(
        DiscipleshipTrack,
        on_delete=models.CASCADE,
        related_name="modules"
    )

    title = models.CharField(max_length=255)

    module_type = models.CharField(
        max_length=50,
        choices=MODULE_TYPES
    )

    duration = models.CharField(max_length=50)

    order = models.PositiveIntegerField(default=1)

    completed = models.BooleanField(default=False)

    locked = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title