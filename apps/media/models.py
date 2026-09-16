from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class MediaAlbum(models.Model):
    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )
    

    description = models.TextField(
        blank=True
    )

    cover_image = models.ImageField(
        upload_to="media/albums/covers/",
        blank=True,
        null=True
    )
    cover_image_source = models.ForeignKey(
        "MediaImage",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+"
    )

    event_date = models.DateField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    featured = models.BooleanField(
        default=False
    )

    published = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "display_order",
            "-event_date",
            "-created_at",
        ]

        verbose_name = "Media Album"
        verbose_name_plural = "Media Albums"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "media:album_detail",
            kwargs={"slug": self.slug}
        )

    @property
    def has_cover(self):
        return bool(self.cover_image)

    def __str__(self):
        return self.title


class MediaImage(models.Model):
    album = models.ForeignKey(
        MediaAlbum,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="media/albums/images/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "display_order",
            "created_at",
        ]

        verbose_name = "Media Image"
        verbose_name_plural = "Media Images"

    def __str__(self):
        return f"{self.album.title} - Image {self.pk}"


class MediaVideo(models.Model):

    VIDEO_TYPE_CHOICES = [
        ("youtube", "YouTube"),
        ("vimeo", "Vimeo"),
        ("external", "External Video"),
    ]

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    thumbnail = models.ImageField(
        upload_to="media/videos/thumbnails/",
        blank=True,
        null=True
    )

    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional YouTube, Vimeo, or external video URL."
    )

    video_type = models.CharField(
        max_length=20,
        choices=VIDEO_TYPE_CHOICES,
        default="youtube"
    )

    duration = models.CharField(
        max_length=20,
        blank=True
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    featured = models.BooleanField(
        default=False
    )

    published = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    views = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "display_order",
            "-published_at",
            "-created_at",
        ]

        verbose_name = "Media Video"
        verbose_name_plural = "Media Videos"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "media:video_detail",
            kwargs={"slug": self.slug}
        )

    def __str__(self):
        return self.title

