from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class NewsCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):

    class ContentType(models.TextChoices):
        ARTICLE = "article", "Article"
        VIDEO = "video", "Video"
        CAMPAIGN = "campaign", "Campaign Update"

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        default=ContentType.ARTICLE
    )

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    excerpt = models.TextField(
        blank=True,
        help_text="Short summary displayed on news cards."
    )

    # =========================================================
    # WRITTEN CONTENT
    # =========================================================

    content = models.TextField(
        blank=True
    )

    # =========================================================
    # IMAGE
    # =========================================================

    featured_image = models.ImageField(
        upload_to="news/images/",
        blank=True,
        null=True
    )

    # =========================================================
    # VIDEO UPLOAD
    # =========================================================

    video = models.FileField(
        upload_to="news/videos/",
        blank=True,
        null=True,
        help_text="Upload an MP4, WebM or other supported video file."
    )

    # =========================================================
    # EXTERNAL VIDEO
    # =========================================================

    video_url = models.URLField(
        blank=True,
        help_text="Optional YouTube, Facebook or other video URL."
    )

    # =========================================================
    # PUBLISHING
    # =========================================================

    published = models.BooleanField(
        default=False
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    # =========================================================
    # STATISTICS
    # =========================================================

    views = models.PositiveIntegerField(
        default=0
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-published_at",
            "-created_at"
        ]

        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        if self.published and not self.published_at:
            self.published_at = timezone.now()

        if not self.published:
            self.published_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    