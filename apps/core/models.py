from django.db import models


class CampaignProfile(models.Model):
    """
    Stores the main campaign/candidate information
    displayed throughout the website.
    """

    candidate_name = models.CharField(
        max_length=150,
        default="Hon. Emem Jackson",
    )

    position = models.CharField(
        max_length=200,
        blank=True,
        help_text="Example: Candidate for Federal House of Representatives",
    )

    campaign_name = models.CharField(
        max_length=150,
        default="UDUAK-ABASI 2027",
    )

    slogan = models.CharField(
        max_length=255,
        blank=True,
    )

    short_bio = models.TextField(
        blank=True,
        help_text="Short biography used on the homepage.",
    )

    biography = models.TextField(
        blank=True,
        help_text="Full biography used on the About page.",
    )

    vision = models.TextField(
        blank=True,
        help_text="Campaign vision statement.",
    )

    mission = models.TextField(
        blank=True,
        help_text="Campaign mission statement.",
    )

    hero_image = models.ImageField(
        upload_to="campaign/",
        blank=True,
        null=True,
        help_text="Main image used in the homepage hero section.",
    )

    profile_image = models.ImageField(
        upload_to="campaign/",
        blank=True,
        null=True,
        help_text="Candidate profile image.",
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    facebook = models.URLField(
        blank=True,
    )

    instagram = models.URLField(
        blank=True,
    )

    x_url = models.URLField(
        blank=True,
        verbose_name="X",
    )

    youtube = models.URLField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only the active campaign profile will be displayed.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Campaign Profile"
        verbose_name_plural = "Campaign Profile"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.candidate_name

class Agenda(models.Model):
    number = models.PositiveIntegerField(
        default=1,
        help_text="Display order of this agenda item."
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        help_text="Short description of this agenda item."
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome icon class, e.g. fa-solid fa-briefcase"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only active agenda items will appear on the website."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Agenda Item"
        verbose_name_plural = "Agenda Items"
        ordering = ["number", "title"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"

class VolunteerApplication(models.Model):

    INTEREST_CHOICES = [
        ("volunteering", "General Volunteering"),
        ("community", "Community Mobilisation"),
        ("youth", "Youth Engagement"),
        ("women", "Women Engagement"),
        ("media", "Media & Communications"),
        ("digital", "Digital & Online Campaign"),
        ("events", "Events & Campaign Activities"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    interest = models.CharField(
        max_length=50,
        choices=INTEREST_CHOICES,
        default="volunteering",
    )

    message = models.TextField(
        blank=True,
    )

    is_contacted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Volunteer Application"
        verbose_name_plural = "Volunteer Applications"

    def __str__(self):
        return f"{self.name} - {self.get_interest_display()}"

