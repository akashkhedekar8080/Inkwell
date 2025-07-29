import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify

# Create your models here.


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimestampModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email"])]

    def __str__(self):
        return self.full_name


class PublishManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def published_at(self, published_at):
        return self.filter(published_at=published_at)


class Status(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    archived = "archived", "Archived"


@deconstructible
class GenerateImagePath:
    def __call__(self, instance, filename):
        return f"posts/{instance.id}/{filename}"


class BlogPost(TimestampModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=GenerateImagePath())
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    excerpt = models.CharField(max_length=500, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        choices=Status.choices, default=Status.DRAFT, max_length=20
    )
    objects = models.Manager()
    publishes = PublishManger()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(BlogPost, self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        if self.content and not self.excerpt:
            self.excerpt = self.content[:247].rsplit(" ", 1)[0] + "..."

        return super().save(*args, **kwargs)

    def generate_unique_slug(self, model_class, title):
        slug = slugify(title)
        base_slug = slug
        counter = 1
        while model_class.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def clean(self):
        if self.status == Status.PUBLISHED:
            if not self.published_at:
                raise ValidationError("Published posts must have a published date.")
            if not self.is_published:
                raise ValidationError(
                    "Post marked as published must have 'is_published=True'"
                )
        return super().clean()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["is_published", "published_at"]),
        ]

    def __str__(self):
        return self.title


class Comment(TimestampModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="comments",
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.full_name if self.author else 'Anonymous'}"
