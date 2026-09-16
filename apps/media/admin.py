from django.contrib import admin

from .models import (
    MediaAlbum,
    MediaImage,
    MediaVideo,
)


class MediaImageInline(admin.TabularInline):

    model = MediaImage

    extra = 3

    fields = (
        "image",
        "caption",
        "alt_text",
        "display_order",
    )


@admin.register(MediaAlbum)
class MediaAlbumAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_date",
        "location",
        "image_count",
        "featured",
        "published",
        "display_order",
        "created_at",
    )

    list_filter = (
        "published",
        "featured",
        "event_date",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "location",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = (
        "featured",
        "published",
        "display_order",
    )

    inlines = [
        MediaImageInline,
    ]

    ordering = (
        "display_order",
        "-event_date",
        "-created_at",
    )

    list_per_page = 25

    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = "Photos"


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):

    list_display = (
        "album",
        "caption",
        "display_order",
        "created_at",
    )

    list_filter = (
        "album",
        "created_at",
    )

    search_fields = (
        "album__title",
        "caption",
        "alt_text",
    )

    list_editable = (
        "display_order",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "album",
        "display_order",
    )


@admin.register(MediaVideo)
class MediaVideoAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "video_type",
        "featured",
        "published",
        "views",
        "published_at",
        "display_order",
    )

    list_filter = (
        "video_type",
        "published",
        "featured",
        "published_at",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "video_url",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "views",
        "created_at",
        "updated_at",
    )

    list_editable = (
        "featured",
        "published",
        "display_order",
    )

    ordering = (
        "display_order",
        "-published_at",
        "-created_at",
    )

    list_per_page = 25