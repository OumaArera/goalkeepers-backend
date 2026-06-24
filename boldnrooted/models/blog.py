import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ScriptureReference(models.Model):
    """
    Stores biblical references like:
    Book: John
    Chapter: 3
    Verse start: 16
    Verse end: 18
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    book = models.CharField(max_length=100)
    chapter = models.PositiveIntegerField()
    verse_start = models.PositiveIntegerField()
    verse_end = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["book"]),
            models.Index(fields=["chapter"]),
        ]

    def __str__(self):
        if self.verse_end:
            return f"{self.book} {self.chapter}:{self.verse_start}-{self.verse_end}"
        return f"{self.book} {self.chapter}:{self.verse_start}"


class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blog_posts"
    )

    content = models.TextField()

    scripture_references = models.ManyToManyField(
        ScriptureReference,
        blank=True,
        related_name="blog_posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="blog_posts"
    )

    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)

            slug = base_slug
            counter = 1

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title