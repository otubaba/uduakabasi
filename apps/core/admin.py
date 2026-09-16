from django.contrib import admin

from .models import CampaignProfile, Agenda, ContactMessage


@admin.register(CampaignProfile)
class CampaignProfileAdmin(admin.ModelAdmin):

    list_display = (
        "candidate_name",
        "campaign_name",
        "position",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "candidate_name",
        "campaign_name",
        "position",
        "slogan",
        "short_bio",
        "biography",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Campaign Identity",
            {
                "fields": (
                    "candidate_name",
                    "position",
                    "campaign_name",
                    "slogan",
                    "is_active",
                )
            },
        ),

        (
            "Biography",
            {
                "fields": (
                    "short_bio",
                    "biography",
                )
            },
        ),

        (
            "Vision & Mission",
            {
                "fields": (
                    "vision",
                    "mission",
                )
            },
        ),

        (
            "Campaign Images",
            {
                "fields": (
                    "hero_image",
                    "profile_image",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                )
            },
        ),

        (
            "Social Media",
            {
                "fields": (
                    "facebook",
                    "instagram",
                    "x_url",
                    "youtube",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):

    list_display = (
        "number",
        "title",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "number",
        "title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Agenda Information",
            {
                "fields": (
                    "number",
                    "title",
                    "description",
                    "icon",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

