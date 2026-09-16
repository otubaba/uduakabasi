from django.contrib import admin

from .models import (
    LocalGovernment,
    Ward,
    PollingUnit,
    EmpowermentProgramme,
    EmpowermentApplication,
    EmpowermentReview,
    EmpowermentBeneficiary,
)


# ============================================================
# CONSTITUENCY LOCATION ADMIN
# ============================================================

@admin.register(LocalGovernment)
class LocalGovernmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "ward_count",
        "application_count",
        "active",
        "display_order",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "code",
    )

    list_editable = (
        "active",
        "display_order",
    )

    ordering = (
        "display_order",
        "name",
    )

    def ward_count(self, obj):
        return obj.wards.count()

    ward_count.short_description = "Wards"

    def application_count(self, obj):
        return obj.empowerment_applications.count()

    application_count.short_description = "Applications"

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "local_government",
        "code",
        "polling_unit_count",
        "application_count",
        "active",
        "display_order",
    )

    list_filter = (
        "local_government",
        "active",
    )

    search_fields = (
        "name",
        "code",
        "local_government__name",
    )

    list_editable = (
        "active",
        "display_order",
    )

    ordering = (
        "local_government",
        "display_order",
        "name",
    )

    def polling_unit_count(self, obj):
        return obj.polling_units.count()

    polling_unit_count.short_description = (
        "Polling Units"
    )

    def application_count(self, obj):
        return obj.empowerment_applications.count()

    application_count.short_description = (
        "Applications"
    )


@admin.register(PollingUnit)
class PollingUnitAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "ward",
        "local_government",
        "polling_unit_type",
        "active",
    )

    list_filter = (
        "polling_unit_type",
        "active",
        "ward__local_government",
    )

    search_fields = (
        "code",
        "name",
        "ward__name",
        "ward__local_government__name",
    )

    list_editable = (
        "active",
    )

    ordering = (
        "ward__local_government",
        "ward",
        "display_order",
    )

    list_per_page = 50

    @admin.display(
        description="Local Government"
    )
    def local_government(self, obj):
        return obj.ward.local_government.name

# ============================================================
# EMPOWERMENT PROGRAMME
# ============================================================

@admin.register(EmpowermentProgramme)
class EmpowermentProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "programme_type",
        "application_start",
        "application_end",
        "active",
        "published",
        "featured",
        "created_at",
    )

    list_filter = (
        "programme_type",
        "active",
        "published",
        "featured",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "eligibility",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "active",
        "published",
        "featured",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25


# ============================================================
# EMPOWERMENT APPLICATION
# ============================================================

@admin.register(EmpowermentApplication)
class EmpowermentApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "application_number",
        "full_name",
        "programme",
        "local_government",
        "ward",
        "community",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "gender",
        "local_government",
        "programme",
        "created_at",
    )

    search_fields = (
        "application_number",
        "first_name",
        "last_name",
        "other_names",
        "phone",
        "email",
        "community",
        "ward",
        "local_government",
    )

    readonly_fields = (
        "application_number",
        "created_at",
        "updated_at",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    fieldsets = (

        (
            "Programme",
            {
                "fields": (
                    "programme",
                    "application_number",
                    "status",
                )
            }
        ),

        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "other_names",
                    "gender",
                    "date_of_birth",
                )
            }
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                )
            }
        ),

        (
            "Constituency Information",
            {
                "fields": (
                    "community",
                    "ward",
                    "local_government",
                    "senatorial_district",
                )
            }
        ),

        (
            "Background",
            {
                "fields": (
                    "occupation",
                    "employment_status",
                    "educational_background",
                )
            }
        ),

        (
            "Application",
            {
                "fields": (
                    "reason_for_applying",
                    "proposed_use",
                    "relevant_experience",
                    "expected_impact",
                )
            }
        ),

        (
            "Review",
            {
                "fields": (
                    "reviewer_notes",
                    "reviewed_at",
                )
            }
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )


# ============================================================
# EMPOWERMENT REVIEW
# ============================================================

@admin.register(EmpowermentReview)
class EmpowermentReviewAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "total_score_display",
        "eligibility_score",
        "need_score",
        "community_impact_score",
        "feasibility_score",
        "experience_score",
        "constituency_balance_score",
        "reviewed_at",
    )

    list_filter = (
        "reviewed_at",
    )

    search_fields = (
        "application__application_number",
        "application__first_name",
        "application__last_name",
    )

    readonly_fields = (
        "total_score_display",
        "created_at",
        "reviewed_at",
    )

    def total_score_display(self, obj):

        return f"{obj.total_score}/100"

    total_score_display.short_description = "Total Score"


# ============================================================
# EMPOWERMENT BENEFICIARY
# ============================================================

@admin.register(EmpowermentBeneficiary)
class EmpowermentBeneficiaryAdmin(admin.ModelAdmin):

    list_display = (
        "beneficiary_number",
        "applicant_name",
        "support_received",
        "delivery_status",
        "delivery_date",
        "created_at",
    )

    list_filter = (
        "delivery_status",
        "delivery_date",
        "created_at",
    )

    search_fields = (
        "beneficiary_number",
        "application__application_number",
        "application__first_name",
        "application__last_name",
        "support_received",
    )

    readonly_fields = (
        "beneficiary_number",
        "created_at",
        "updated_at",
    )

    list_editable = (
        "delivery_status",
    )

    ordering = (
        "-created_at",
    )

    def applicant_name(self, obj):

        return obj.application.full_name

    applicant_name.short_description = "Beneficiary"

