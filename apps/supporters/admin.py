from django.contrib import admin

from .models import Supporter


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone",
        "email",
        "lga",
        "ward",
        "community",
        "volunteer",
        "status",
        "registered_at",
    )

    list_filter = (
        "status",
        "gender",
        "volunteer",
        "receive_updates",
        "lga",
        "registered_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "lga",
        "ward",
        "community",
        "occupation",
        "skills",
    )

    list_editable = (
        "status",
        "volunteer",
    )

    readonly_fields = (
        "registered_at",
        "updated_at",
    )

    date_hierarchy = "registered_at"

    ordering = (
        "-registered_at",
    )

    fieldsets = (

        (
            "Personal Information",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "email",
                    "gender",
                    "date_of_birth",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "lga",
                    "ward",
                    "community",
                    "address",
                )
            },
        ),

        (
            "Participation",
            {
                "fields": (
                    "occupation",
                    "volunteer",
                    "skills",
                    "receive_updates",
                )
            },
        ),

        (
            "Administration",
            {
                "fields": (
                    "status",
                    "notes",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "registered_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

