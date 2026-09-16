from django.contrib import admin

from .models import NewsArticle, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "content_type",
        "category",
        "published",
        "published_at",
        "views",
        "created_at",
    )

    list_filter = (
        "content_type",
        "category",
        "published",
        "published_at",
    )

    search_fields = (
        "title",
        "excerpt",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "views",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-published_at",
        "-created_at",
    )

    