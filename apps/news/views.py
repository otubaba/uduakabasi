from urllib.parse import parse_qs, urlparse

from django.db.models import F
from django.views.generic import ListView, DetailView

from .models import NewsArticle
from apps.core.models import CampaignProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class NewsManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_active
            and (
                self.request.user.is_superuser
                or self.request.user.groups.filter(
                    name="News Manager"
                ).exists()
            )
        )

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(
            self.request,
            "You do not have permission to manage news."
        )

        return redirect("dashboard:home")

    
# =========================================================
# NEWS LIST
# =========================================================

class NewsListView(ListView):

    model = NewsArticle
    template_name = "news/list.html"
    context_object_name = "news_articles"
    paginate_by = 9

    def get_queryset(self):

        return (
            NewsArticle.objects
            .filter(
                published=True
            )
            .select_related(
                "category"
            )
            .order_by(
                "-published_at",
                "-created_at",
            )
        )


# =========================================================
# NEWS DETAIL
# =========================================================

class NewsDetailView(DetailView):

    model = NewsArticle
    template_name = "news/detail.html"
    context_object_name = "article"

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):

        return (
            NewsArticle.objects
            .filter(
                published=True
            )
            .select_related(
                "category"
            )
        )

    # -----------------------------------------------------
    # INCREMENT VIEWS
    # -----------------------------------------------------

    def get_object(self, queryset=None):

        article = super().get_object(queryset)

        NewsArticle.objects.filter(
            pk=article.pk
        ).update(
            views=F("views") + 1
        )

        article.refresh_from_db(
            fields=["views"]
        )

        return article

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        article = self.object

        context["profile"] = CampaignProfile.objects.filter(
            is_active=True
        ).first()

        context["video_embed_url"] = (
            self.get_video_embed_url(
                article.video_url
            )
        )

        # -------------------------------------------------
        # RELATED ARTICLES
        # -------------------------------------------------

        if article.category:

            context["related_articles"] = (
                NewsArticle.objects
                .filter(
                    published=True,
                    category=article.category,
                )
                .exclude(
                    pk=article.pk
                )
                .select_related(
                    "category"
                )
                .order_by(
                    "-published_at",
                    "-created_at",
                )[:3]
            )

        else:

            context["related_articles"] = (
                NewsArticle.objects
                .filter(
                    published=True,
                )
                .exclude(
                    pk=article.pk
                )
                .select_related(
                    "category"
                )
                .order_by(
                    "-published_at",
                    "-created_at",
                )[:3]
            )

        return context

    # -----------------------------------------------------
    # VIDEO URL CONVERTER
    # -----------------------------------------------------

    @staticmethod
    def get_video_embed_url(url):

        if not url:
            return None

        parsed_url = urlparse(url)

        hostname = (
            parsed_url.hostname or ""
        ).lower()

        # =================================================
        # YOUTUBE STANDARD URL
        # =================================================
        #
        # https://www.youtube.com/watch?v=VIDEO_ID
        #

        if hostname in (
            "www.youtube.com",
            "youtube.com",
            "m.youtube.com",
        ):

            query = parse_qs(
                parsed_url.query
            )

            video_id = query.get("v")

            if video_id:

                return (
                    "https://www.youtube.com/embed/"
                    f"{video_id[0]}"
                )

        # =================================================
        # YOUTUBE SHORT URL
        # =================================================
        #
        # https://youtu.be/VIDEO_ID
        #

        if hostname in (
            "youtu.be",
            "www.youtu.be",
        ):

            video_id = (
                parsed_url.path
                .strip("/")
            )

            if video_id:

                return (
                    "https://www.youtube.com/embed/"
                    f"{video_id}"
                )

        # =================================================
        # YOUTUBE SHORTS
        # =================================================
        #
        # https://www.youtube.com/shorts/VIDEO_ID
        #

        if hostname in (
            "www.youtube.com",
            "youtube.com",
        ):

            path_parts = (
                parsed_url.path
                .strip("/")
                .split("/")
            )

            if (
                len(path_parts) >= 2
                and path_parts[0] == "shorts"
            ):

                return (
                    "https://www.youtube.com/embed/"
                    f"{path_parts[1]}"
                )

        return None
    