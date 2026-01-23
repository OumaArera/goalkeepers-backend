import uuid
from django.db import models
from django.conf import settings


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="player_profile"
    )

    avatar = models.ImageField(
        upload_to="players/avatars/",
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    middle_names = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    country_of_birth = models.CharField(max_length=100)
    country_of_residence = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["last_name"]),
            models.Index(fields=["country_of_birth"]),
            models.Index(fields=["country_of_residence"]),
        ]
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
