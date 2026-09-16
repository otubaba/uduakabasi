from urllib.parse import parse_qs, urlparse

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import (
    DetailView,
    ListView, CreateView, UpdateView, DeleteView
)
from .forms import (
    MediaAlbumForm,
    MediaImageForm,
    MediaVideoForm,
    MediaBulkImageUploadForm,
)
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import MediaAlbum, MediaImage, MediaVideo
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render

class MediaManagerRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin
    ):
    def test_func(self):
        return (
        self.request.user.is_active
        and (
        self.request.user.is_superuser
        or self.request.user.groups.filter(
        name="Gallery Manager"
        ).exists()
        )
    )

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You do not have permission to manage media."
        )

        return redirect("dashboard:home")


class AlbumListView(ListView):
    model = MediaAlbum
    template_name = "media/gallery.html"
    context_object_name = "albums"
    paginate_by = 12

    def get_queryset(self):
        return (
            MediaAlbum.objects
            .filter(published=True)
            .annotate(
                image_count=Count("images")
            )
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=MediaImage.objects.order_by(
                        "display_order",
                        "created_at"
                    )
                )
            )
            .order_by(
                "display_order",
                "-event_date",
                "-created_at"
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_albums"] = (
            MediaAlbum.objects
            .filter(
                published=True,
                featured=True
            )
            .annotate(
                image_count=Count("images")
            )
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=MediaImage.objects.order_by(
                        "display_order",
                        "created_at"
                    )
                )
            )
            .order_by(
                "display_order",
                "-event_date",
                "-created_at"
            )[:3]
        )

        return context


class AlbumDetailView(DetailView):
    model = MediaAlbum
    template_name = "media/album_detail.html"
    context_object_name = "album"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            MediaAlbum.objects
            .filter(published=True)
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=MediaImage.objects.order_by(
                        "display_order",
                        "created_at"
                    )
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        album = self.object

        context["images"] = album.images.all()

        context["related_albums"] = (
            MediaAlbum.objects
            .filter(
                published=True
            )
            .exclude(
                pk=album.pk
            )
            .annotate(
                image_count=Count("images")
            )
            .order_by(
                "display_order",
                "-event_date",
                "-created_at"
            )[:4]
        )

        return context

class VideoListView(ListView):

    model = MediaVideo

    template_name = "media/videos.html"

    context_object_name = "videos"

    paginate_by = 9

    def get_queryset(self):

        return (
            MediaVideo.objects
            .filter(published=True)
            .order_by(
                "display_order",
                "-published_at",
                "-created_at",
            )
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["featured_videos"] = (
            MediaVideo.objects
            .filter(
                published=True,
                featured=True,
            )
            .order_by(
                "display_order",
                "-published_at",
            )[:3]
        )

        return context


class VideoDetailView(DetailView):

    model = MediaVideo

    template_name = "media/video_detail.html"

    context_object_name = "video"

    slug_field = "slug"

    slug_url_kwarg = "slug"

    def get_queryset(self):

        return MediaVideo.objects.filter(
            published=True
        )

    def get_object(self, queryset=None):

        video = super().get_object(queryset)

        MediaVideo.objects.filter(
            pk=video.pk
        ).update(
            views=F("views") + 1
        )

        # Refresh the object so the template receives
        # the actual database value.
        video.refresh_from_db(
            fields=["views"]
        )

        return video

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        video = self.object

        context["embed_url"] = self.get_embed_url(
            video.video_url,
            video.video_type,
        )

        context["related_videos"] = (
            MediaVideo.objects
            .filter(
                published=True
            )
            .exclude(
                pk=video.pk
            )
            .order_by(
                "display_order",
                "-published_at",
                "-created_at",
            )[:3]
        )

        return context

    @staticmethod
    def get_embed_url(url, video_type):

        if not url:
            return None

        parsed = urlparse(url)

        # =====================================================
        # YOUTUBE
        # =====================================================

        if video_type == "youtube":

            if parsed.hostname in (
                "youtube.com",
                "www.youtube.com",
                "m.youtube.com",
            ):

                query = parse_qs(
                    parsed.query
                )

                video_id = query.get("v")

                if video_id:

                    return (
                        "https://www.youtube.com/embed/"
                        + video_id[0]
                    )

                path_parts = (
                    parsed.path
                    .strip("/")
                    .split("/")
                )

                if (
                    len(path_parts) >= 2
                    and path_parts[0] in (
                        "shorts",
                        "embed",
                    )
                ):

                    return (
                        "https://www.youtube.com/embed/"
                        + path_parts[1]
                    )

            if parsed.hostname in (
                "youtu.be",
                "www.youtu.be",
            ):

                video_id = (
                    parsed.path
                    .strip("/")
                )

                if video_id:

                    return (
                        "https://www.youtube.com/embed/"
                        + video_id
                    )

        # =====================================================
        # VIMEO
        # =====================================================

        if video_type == "vimeo":

            if parsed.hostname in (
                "vimeo.com",
                "www.vimeo.com",
            ):

                video_id = (
                    parsed.path
                    .strip("/")
                    .split("/")[-1]
                )

                if video_id.isdigit():

                    return (
                        "https://player.vimeo.com/video/"
                        + video_id
                    )

        # =====================================================
        # EXTERNAL VIDEO
        # =====================================================

        if video_type == "external":

            return url

        return None

# ============================================================
# MEDIA MANAGER DASHBOARD
# ============================================================

class MediaDashboardView(
    MediaManagerRequiredMixin,
    TemplateView
):
    template_name = "dashboard/media/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ====================================================
        # ALBUM COUNTS
        # ====================================================

        context["total_albums"] = MediaAlbum.objects.count()

        context["published_albums"] = (
            MediaAlbum.objects
            .filter(published=True)
            .count()
        )

        context["draft_albums"] = (
            MediaAlbum.objects
            .filter(published=False)
            .count()
        )

        context["featured_albums"] = (
            MediaAlbum.objects
            .filter(featured=True)
            .count()
        )

        # ====================================================
        # PHOTO COUNTS
        # ====================================================

        context["total_images"] = MediaImage.objects.count()

        # ====================================================
        # VIDEO COUNTS
        # ====================================================

        context["total_videos"] = MediaVideo.objects.count()

        context["published_videos"] = (
            MediaVideo.objects
            .filter(published=True)
            .count()
        )

        context["draft_videos"] = (
            MediaVideo.objects
            .filter(published=False)
            .count()
        )

        context["featured_videos"] = (
            MediaVideo.objects
            .filter(featured=True)
            .count()
        )

        # ====================================================
        # RECENT ALBUMS
        # ====================================================

        context["recent_albums"] = (
            MediaAlbum.objects
            .annotate(
                image_count=Count("images")
            )
            .order_by("-created_at")[:5]
        )

        # ====================================================
        # RECENT VIDEOS
        # ====================================================

        context["recent_videos"] = (
            MediaVideo.objects
            .order_by("-created_at")[:5]
        )

        # ====================================================
        # RECENT IMAGES
        # ====================================================

        context["recent_images"] = (
            MediaImage.objects
            .select_related("album")
            .order_by("-created_at")[:8]
        )

        return context
    
# ============================================================
# MEDIA ALBUM MANAGEMENT
# ============================================================
class MediaAlbumListView(MediaManagerRequiredMixin, ListView):
    model = MediaAlbum
    template_name = "dashboard/media/album_list.html"
    context_object_name = "albums"
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            MediaAlbum.objects
            .annotate(image_count=Count("images"))
            .order_by("-created_at")
        )

        search = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        if search:
            queryset = queryset.filter(title__icontains=search)

        if status == "published":
            queryset = queryset.filter(published=True)

        elif status == "draft":
            queryset = queryset.filter(published=False)

        return queryset

class MediaAlbumDetailView(DetailView):
    model = MediaAlbum
    template_name = "media/album_detail.html"
    context_object_name = "album"

    def get_queryset(self):
        return (
            MediaAlbum.objects
            .filter(published=True)
            .prefetch_related("images")
        )

class MediaAlbumCreateView(
    MediaManagerRequiredMixin,
    CreateView
):
    model = MediaAlbum
    form_class = MediaAlbumForm
    template_name = "dashboard/media/album_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "media:album_manage",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Media album created successfully."
        )
        return super().form_valid(form)


class MediaAlbumUpdateView(
    MediaManagerRequiredMixin,
    UpdateView
):
    model = MediaAlbum
    form_class = MediaAlbumForm
    template_name = "dashboard/media/album_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "media:album_manage",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Media album updated successfully."
        )
        return super().form_valid(form)

class MediaAlbumManageView(
    MediaManagerRequiredMixin,
    DetailView
):
    model = MediaAlbum
    template_name = "dashboard/media/album_manage.html"
    context_object_name = "object"

    def get_queryset(self):
        return (
            MediaAlbum.objects
            .prefetch_related("images")
        )

class MediaAlbumDeleteView(
    MediaManagerRequiredMixin,
    DeleteView
):
    model = MediaAlbum
    template_name = "dashboard/media/album_delete.html"
    success_url = reverse_lazy("media:dashboard")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Media album deleted successfully."
        )
        return super().form_valid(form)

# ============================================================
# BULK IMAGE UPLOAD
# ============================================================

class MediaBulkImageUploadView(
    MediaManagerRequiredMixin,
    TemplateView
):
    template_name = "dashboard/media/image_upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["album"] = MediaAlbum.objects.get(
            pk=self.kwargs["pk"]
        )

        context["form"] = MediaBulkImageUploadForm()

        return context

    def post(self, request, *args, **kwargs):

        album = MediaAlbum.objects.get(
            pk=self.kwargs["pk"]
        )

        form = MediaBulkImageUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            images = form.cleaned_data["images"]

            start_order = (
                album.images.count()
            )

            for index, image in enumerate(images):

                MediaImage.objects.create(
                    album=album,
                    image=image,
                    display_order=start_order + index,
                )

            messages.success(
                request,
                f"{len(images)} image(s) uploaded successfully."
            )

            return redirect(
                "media:album_manage",
                pk=album.pk,
            )

        return render(
            request,
            self.template_name,
            {
                "album": album,
                "form": form,
            },
        )


class MediaImageUpdateView(MediaManagerRequiredMixin, UpdateView):
    model = MediaImage
    form_class = MediaImageForm
    template_name = "dashboard/media/image_form.html"
    context_object_name = "image"

    def get_success_url(self):
        return reverse_lazy(
            "media:album_manage",
            kwargs={"pk": self.object.album.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Photo information updated successfully.",
        )
        return super().form_valid(form)


class MediaImageDeleteView(MediaManagerRequiredMixin, DeleteView):
    model = MediaImage
    template_name = "dashboard/media/image_delete.html"
    context_object_name = "image"

    def get_success_url(self):
        return reverse_lazy(
            "media:album_manage",
            kwargs={"pk": self.object.album.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Photo deleted successfully.",
        )
        return super().form_valid(form)
    
# ============================================================
# VIDEO MANAGEMENT
# ============================================================

class MediaVideoListView(MediaManagerRequiredMixin, ListView):
    model = MediaVideo
    template_name = "dashboard/media/video_list.html"
    context_object_name = "videos"
    paginate_by = 15

    def get_queryset(self):
        queryset = MediaVideo.objects.all().order_by(
            "-created_at"
        )

        search = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        if status == "published":
            queryset = queryset.filter(published=True)

        elif status == "draft":
            queryset = queryset.filter(published=False)

        return queryset


class MediaVideoCreateView(MediaManagerRequiredMixin, CreateView):
    model = MediaVideo
    form_class = MediaVideoForm
    template_name = "dashboard/media/video_form.html"

    def get_success_url(self):
        return reverse_lazy("media:video_manage")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Video created successfully."
        )
        return super().form_valid(form)


class MediaVideoManageView(MediaManagerRequiredMixin, DetailView):
    model = MediaVideo
    template_name = "dashboard/media/video_manage.html"
    context_object_name = "object"


class MediaVideoUpdateView(MediaManagerRequiredMixin, UpdateView):
    model = MediaVideo
    form_class = MediaVideoForm
    template_name = "dashboard/media/video_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "media:video_manage",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Video updated successfully."
        )
        return super().form_valid(form)


class MediaVideoDeleteView(MediaManagerRequiredMixin, DeleteView):
    model = MediaVideo
    template_name = "dashboard/media/video_delete.html"
    context_object_name = "video"
    success_url = reverse_lazy("media:video_manage")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Video deleted successfully."
        )
        return super().form_valid(form)

