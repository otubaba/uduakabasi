from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ============================================================
# CONSTITUENCY LOCATION MODELS
# ============================================================

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class LocalGovernment(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    active = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Local Government"
        verbose_name_plural = "Local Governments"

    def __str__(self):
        return self.name


class Ward(models.Model):
    local_government = models.ForeignKey(
        LocalGovernment,
        on_delete=models.CASCADE,
        related_name="wards",
    )

    name = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=20,
    )

    active = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Ward"
        verbose_name_plural = "Wards"

        constraints = [
            models.UniqueConstraint(
                fields=["local_government", "code"],
                name="unique_ward_code_per_lga",
            ),
        ]

    def __str__(self):
        return f"{self.local_government.name} — {self.name}"


class PollingUnit(models.Model):
    POLLING_UNIT_TYPE_CHOICES = [
        ("existing", "Existing PU"),
        ("new", "New PU"),
    ]

    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name="polling_units",
    )

    code = models.CharField(
        max_length=50,
    )

    name = models.CharField(
        max_length=255,
    )

    polling_unit_type = models.CharField(
        max_length=20,
        choices=POLLING_UNIT_TYPE_CHOICES,
        default="existing",
    )

    active = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "code",
        ]

        verbose_name = "Polling Unit"
        verbose_name_plural = "Polling Units"

        constraints = [
            models.UniqueConstraint(
                fields=["ward", "code"],
                name="unique_polling_unit_code_per_ward",
            ),
        ]

    def __str__(self):
        return f"{self.code} — {self.name}"
# ============================================================
# EMPOWERMENT PROGRAMME
# ============================================================

class EmpowermentProgramme(models.Model):

    PROGRAMME_TYPE_CHOICES = [
        ("skills", "Skills Training"),
        ("business", "Business Support"),
        ("agriculture", "Agricultural Support"),
        ("education", "Educational Support"),
        ("equipment", "Equipment Support"),
        ("employment", "Employment Support"),
        ("women", "Women Empowerment"),
        ("youth", "Youth Empowerment"),
        ("other", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    description = models.TextField()

    programme_type = models.CharField(
        max_length=30,
        choices=PROGRAMME_TYPE_CHOICES,
        default="other"
    )

    eligibility = models.TextField(
        blank=True
    )

    application_start = models.DateTimeField(
        blank=True,
        null=True
    )

    application_end = models.DateTimeField(
        blank=True,
        null=True
    )

    maximum_applicants = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    published = models.BooleanField(
        default=False
    )

    active = models.BooleanField(
        default=True
    )

    featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

        verbose_name = "Empowerment Programme"

        verbose_name_plural = "Empowerment Programmes"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse(
            "empowerment:programme_detail",
            kwargs={
                "slug": self.slug
            }
        )


# ============================================================
# EMPOWERMENT APPLICATION
# ============================================================

class EmpowermentApplication(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("shortlisted", "Shortlisted"),
        ("approved", "Approved"),
        ("waitlisted", "Waitlisted"),
        ("not_selected", "Not Selected"),
        ("completed", "Completed"),
        ("withdrawn", "Withdrawn"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    programme = models.ForeignKey(
        EmpowermentProgramme,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    application_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    other_names = models.CharField(
        max_length=100,
        blank=True,
    )

    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=30,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.CharField(
        max_length=255,
    )

    community = models.CharField(
        max_length=150,
    )

    local_government = models.ForeignKey(
        LocalGovernment,
        on_delete=models.PROTECT,
        related_name="empowerment_applications",
    )

    ward = models.ForeignKey(
        Ward,
        on_delete=models.PROTECT,
        related_name="empowerment_applications",
    )

    polling_unit = models.ForeignKey(
        PollingUnit,
        on_delete=models.PROTECT,
        related_name="empowerment_applications",
    )

    vin = models.CharField(
        max_length=50,
        blank=True,
        help_text="Voters Identification Number (VIN)",
    )

    senatorial_district = models.CharField(
        max_length=150,
        default="Uyo Senatorial District",
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
    )

    employment_status = models.CharField(
        max_length=150,
        blank=True,
    )

    educational_background = models.CharField(
        max_length=255,
        blank=True,
    )

    reason_for_applying = models.TextField()

    proposed_use = models.TextField(
        blank=True,
    )

    relevant_experience = models.TextField(
        blank=True,
    )

    expected_impact = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="submitted",
    )

    reviewer_notes = models.TextField(
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        verbose_name = "Empowerment Application"
        verbose_name_plural = "Empowerment Applications"

        indexes = [
            models.Index(
                fields=["status"]
            ),
            models.Index(
                fields=["local_government"]
            ),
            models.Index(
                fields=["ward"]
            ),
            models.Index(
                fields=["polling_unit"]
            ),
            models.Index(
                fields=["community"]
            ),
            models.Index(
                fields=["created_at"]
            ),
        ]

    def __str__(self):
        return f"{self.application_number} - {self.full_name}"

    @property
    def full_name(self):
        names = [
            self.first_name,
            self.other_names,
            self.last_name,
        ]

        return " ".join(
            name.strip()
            for name in names
            if name and name.strip()
        )

    def save(self, *args, **kwargs):

        if not self.application_number:

            super().save(*args, **kwargs)

            self.application_number = (
                f"UAB-EMP-{self.pk:06d}"
            )

            super().save(
                update_fields=[
                    "application_number"
                ]
            )

            return

        super().save(*args, **kwargs)

# ============================================================
# EMPOWERMENT REVIEW
# ============================================================

class EmpowermentReview(models.Model):

    application = models.OneToOneField(
        EmpowermentApplication,
        on_delete=models.CASCADE,
        related_name="review"
    )

    eligibility_score = models.PositiveIntegerField(
        default=0
    )

    need_score = models.PositiveIntegerField(
        default=0
    )

    community_impact_score = models.PositiveIntegerField(
        default=0
    )

    feasibility_score = models.PositiveIntegerField(
        default=0
    )

    experience_score = models.PositiveIntegerField(
        default=0
    )

    constituency_balance_score = models.PositiveIntegerField(
        default=0
    )

    reviewer_comment = models.TextField(
        blank=True
    )

    reviewed_at = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-reviewed_at"
        ]

        verbose_name = "Empowerment Review"

        verbose_name_plural = "Empowerment Reviews"

    @property
    def total_score(self):

        return (
            self.eligibility_score
            + self.need_score
            + self.community_impact_score
            + self.feasibility_score
            + self.experience_score
            + self.constituency_balance_score
        )

    def __str__(self):

        return (
            f"{self.application.application_number} "
            f"- {self.total_score}/100"
        )


# ============================================================
# EMPOWERMENT BENEFICIARY
# ============================================================

class EmpowermentBeneficiary(models.Model):

    DELIVERY_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scheduled", "Scheduled"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    application = models.OneToOneField(
        EmpowermentApplication,
        on_delete=models.PROTECT,
        related_name="beneficiary_record"
    )

    beneficiary_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        editable=False
    )

    support_received = models.CharField(
        max_length=255
    )

    support_description = models.TextField(
        blank=True
    )

    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default="pending"
    )

    delivery_date = models.DateField(
        blank=True,
        null=True
    )

    follow_up_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Empowerment Beneficiary"

        verbose_name_plural = "Empowerment Beneficiaries"

    def __str__(self):

        return (
            f"{self.beneficiary_number} - "
            f"{self.application.full_name}"
        )

    def save(self, *args, **kwargs):

        if not self.beneficiary_number:

            super().save(*args, **kwargs)

            self.beneficiary_number = (
                f"UAB-BEN-{self.pk:06d}"
            )

            super().save(
                update_fields=[
                    "beneficiary_number"
                ]
            )

            return

        super().save(*args, **kwargs)



