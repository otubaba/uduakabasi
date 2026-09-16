from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Event(models.Model):

    # =========================================================
    # EVENT STATUS
    # =========================================================

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    short_description = models.TextField(
        blank=True,
        help_text="Short summary displayed on event cards."
    )

    description = models.TextField(
        blank=True,
        help_text="Full description of the event."
    )

    # =========================================================
    # EVENT IMAGE
    # =========================================================

    featured_image = models.ImageField(
        upload_to="events/images/",
        blank=True,
        null=True
    )

    # =========================================================
    # DATE & TIME
    # =========================================================

    event_date = models.DateField()

    start_time = models.TimeField(
        blank=True,
        null=True
    )

    end_time = models.TimeField(
        blank=True,
        null=True
    )

    # =========================================================
    # LOCATION
    # =========================================================

    venue = models.CharField(
        max_length=255,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Etinan LGA, Akwa Ibom State"
    )

    address = models.TextField(
        blank=True
    )

    # =========================================================
    # EVENT STATUS
    # =========================================================

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING
    )

    # =========================================================
    # REGISTRATION
    # =========================================================

    registration_open = models.BooleanField(
        default=False,
        help_text="Enable registration for this event."
    )

    registration_url = models.URLField(
        blank=True,
        help_text="Optional external registration link."
    )

    # =========================================================
    # WEBSITE DISPLAY
    # =========================================================

    featured = models.BooleanField(
        default=False,
        help_text="Featured events receive prominent placement."
    )

    published = models.BooleanField(
        default=True
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

    # =========================================================
    # META
    # =========================================================

    class Meta:

        ordering = [
            "event_date",
            "start_time",
            "-created_at",
        ]

        verbose_name = "Campaign Event"
        verbose_name_plural = "Campaign Events"

    # =========================================================
    # SAVE
    # =========================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.title
            )

        super().save(
            *args,
            **kwargs
        )

    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):

        return self.title

    # =========================================================
    # HELPER PROPERTIES
    # =========================================================

    @property
    def is_past(self):

        return self.event_date < timezone.localdate()

    @property
    def is_today(self):

        return self.event_date == timezone.localdate()