import uuid
from django.db import models


class Program(models.Model):
    """
    Represents an event or program, such as a retreat, workshop, or seminar.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    organizer = models.CharField(max_length=255)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    location = models.CharField(max_length=255, blank=True)
    
    poster = models.ImageField(
        upload_to="program_posters/",
        blank=True,
        null=True,
        help_text="Optional image for the program poster"
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
        ]

    def __str__(self):
        return self.title