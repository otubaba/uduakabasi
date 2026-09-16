from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    # =========================================================
    # LIST DISPLAY
    # =========================================================

    list_display = (
        "title",
        "event_date",
        "start_time",
        "venue",
        "status",
        "registration_open",
        "featured",
        "published",
    )

    # =========================================================
    # FILTERS
    # =========================================================

    list_filter = (
        "status",
        "registration_open",
        "featured",
        "published",
        "event_date",
    )

    # =========================================================
    # SEARCH
    # =========================================================

    search_fields = (
        "title",
        "short_description",
        "description",
        "venue",
        "location",
        "address",
    )

    # =========================================================
    # EDIT DIRECTLY FROM LIST
    # =========================================================

    list_editable = (
        "status",
        "registration_open",
        "featured",
        "published",
    )

    # =========================================================
    # READ ONLY
    # =========================================================

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    # =========================================================
    # DATE NAVIGATION
    # =========================================================

    date_hierarchy = "event_date"

    # =========================================================
    # ORDERING
    # =========================================================

    ordering = (
        "event_date",
        "start_time",
        "-created_at",
    )

    # =========================================================
    # FORM FIELDSETS
    # =========================================================

    fieldsets = (

        (
            "Event Information",
            {
                "fields": (
                    "title",
                    "short_description",
                    "description",
                    "featured_image",
                )
            },
        ),

        (
            "Date & Time",
            {
                "fields": (
                    "event_date",
                    "start_time",
                    "end_time",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "venue",
                    "location",
                    "address",
                )
            },
        ),

        (
            "Registration",
            {
                "fields": (
                    "registration_open",
                    "registration_url",
                )
            },
        ),

        (
            "Publishing",
            {
                "fields": (
                    "status",
                    "featured",
                    "published",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "slug",
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

