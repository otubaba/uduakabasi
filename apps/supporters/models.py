from django.db import models
from django.utils import timezone


class Supporter(models.Model):

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"
        PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        CONTACTED = "contacted", "Contacted"
        INACTIVE = "inactive", "Inactive"

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=30,
        unique=True
    )

    email = models.EmailField(
        blank=True
    )

    gender = models.CharField(
        max_length=30,
        choices=Gender.choices,
        blank=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    lga = models.CharField(
        max_length=100,
        blank=True
    )

    ward = models.CharField(
        max_length=100,
        blank=True
    )

    community = models.CharField(
        max_length=150,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    occupation = models.CharField(
        max_length=150,
        blank=True
    )

    volunteer = models.BooleanField(
        default=False,
        help_text="Supporter is interested in volunteering."
    )

    skills = models.TextField(
        blank=True,
        help_text="Optional skills or areas where the supporter can contribute."
    )

    receive_updates = models.BooleanField(
        default=True,
        help_text="Supporter agrees to receive campaign updates."
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    notes = models.TextField(
        blank=True,
        help_text="Internal administrative notes."
    )

    registered_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-registered_at"
        ]

        verbose_name = "Supporter"

        verbose_name_plural = "Supporters"

    def __str__(self):
        return self.full_name

