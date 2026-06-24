import uuid
from django.db import models
from django.utils.text import slugify


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    title = models.CharField(max_length=255)

    event_type = models.CharField(
        max_length=100
    )

    event_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=255)

    format = models.CharField(
        max_length=50,
        help_text="Online, Physical, Hybrid"
    )

    capacity = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    description = models.TextField()

    speakers = models.JSONField(
        default=list,
        blank=True
    )

    gradient = models.CharField(max_length=255)

    accent_gradient = models.CharField(max_length=255)

    accent = models.CharField(max_length=20)

    featured = models.BooleanField(default=False)

    registration_open = models.BooleanField(default=True)

    banner = models.ImageField(
        upload_to="event_banners/",
        blank=True,
        null=True
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="events"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-event_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)

            slug = base_slug
            counter = 1

            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title