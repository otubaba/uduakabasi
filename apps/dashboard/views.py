from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    DetailView
)
from django.core.files import File
from django.db import transaction
import json
from apps.events.models import Event
from apps.media.models import MediaAlbum
from apps.news.forms import NewsArticleForm
from apps.news.models import NewsArticle
from apps.supporters.mixins import StaffRequiredMixin
from apps.supporters.models import Supporter
from django.http import JsonResponse
from apps.events.forms import EventForm
from apps.events.models import Event

from apps.media.models import (
    MediaAlbum,
    MediaImage,
    MediaVideo,
)
from apps.core.models import Agenda
from apps.media.forms import (
    MediaAlbumForm,
    MediaImageForm,
    MediaBulkImageUploadForm,
    MediaVideoForm,
)
from django.views import View
from apps.news.views import NewsManagerRequiredMixin
from apps.events.views import EventsManagerRequiredMixin
from apps.empowerment.models import EmpowermentApplication
# =========================================================
# DASHBOARD HOME
# =========================================================

class DashboardHomeView(
    StaffRequiredMixin,
    TemplateView
):

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # -------------------------------------------------
        # SUPPORTERS
        # -------------------------------------------------

        context["total_supporters"] = (
            Supporter.objects.count()
        )

        context["pending_supporters"] = (
            Supporter.objects.filter(
                status=Supporter.Status.PENDING
            ).count()
        )

        context["approved_supporters"] = (
            Supporter.objects.filter(
                status=Supporter.Status.APPROVED
            ).count()
        )

        context["volunteer_count"] = (
            Supporter.objects.filter(
                volunteer=True
            ).count()
        )

        # -------------------------------------------------
        # NEWS
        # -------------------------------------------------

        context["published_news"] = (
            NewsArticle.objects.filter(
                published=True
            ).count()
        )

        context["draft_news"] = (
            NewsArticle.objects.filter(
                published=False
            ).count()
        )

        context["recent_news"] = (
            NewsArticle.objects
            .filter(published=True)
            .select_related("category")
            .order_by(
                "-published_at",
                "-created_at",
            )[:5]
        )

        # -------------------------------------------------
        # EVENTS
        # -------------------------------------------------

        context["upcoming_event_count"] = (
            Event.objects.filter(
                published=True,
                status=Event.Status.UPCOMING,
            ).count()
        )

        context["upcoming_events"] = (
            Event.objects.filter(
                published=True,
                status=Event.Status.UPCOMING,
            )
            .order_by(
                "event_date",
                "start_time",
            )[:5]
        )

        # -------------------------------------------------
        # MEDIA
        # -------------------------------------------------

        # Published gallery albums
        context["gallery_album_count"] = (
            MediaAlbum.objects.filter(
                published=True
            ).count()
        )

        # Total gallery images
        context["gallery_image_count"] = (
            MediaImage.objects.count()
        )

        # Total videos
        context["media_video_count"] = (
            MediaVideo.objects.count()
        )

        # Published videos
        context["published_video_count"] = (
            MediaVideo.objects.filter(
                published=True
            ).count()
        )

        # Draft videos
        context["draft_video_count"] = (
            MediaVideo.objects.filter(
                published=False
            ).count()
        )

        # Featured videos
        context["featured_video_count"] = (
            MediaVideo.objects.filter(
                featured=True,
                published=True
            ).count()
        )

        # Recent albums
        context["recent_media_albums"] = (
            MediaAlbum.objects
            .order_by("-created_at")[:5]
        )

        # Recent videos
        context["recent_media_videos"] = (
            MediaVideo.objects
            .order_by("-created_at")[:5]
        )

        # -------------------------------------------------
        # EMPOWERMENT
        # -------------------------------------------------

        # Total applications
        context["total_empowerment_applications"] = (
            EmpowermentApplication.objects.count()
        )

        # Pending applications
        context["pending_empowerment_applications"] = (
            EmpowermentApplication.objects.filter(
                status="pending"
            ).count()
        )

        # Approved applications
        context["approved_empowerment_applications"] = (
            EmpowermentApplication.objects.filter(
                status="approved"
            ).count()
        )

        # Rejected applications
        context["rejected_empowerment_applications"] = (
            EmpowermentApplication.objects.filter(
                status="rejected"
            ).count()
        )

        # Recent applications
        context["recent_empowerment_applications"] = (
            EmpowermentApplication.objects
            .select_related(
                "programme",
                "local_government",
                "ward",
                "polling_unit",
            )
            .order_by("-created_at")[:5]
        )

        # -------------------------------------------------
        # RECENT SUPPORTERS
        # -------------------------------------------------

        context["recent_supporters"] = (
            Supporter.objects
            .order_by("-registered_at")[:5]
        )

        return context

# =========================================================
# NEWS LIST
# =========================================================

class DashboardNewsListView(
    NewsManagerRequiredMixin,
    ListView
):

    model = NewsArticle

    template_name = "dashboard/news/list.html"

    context_object_name = "articles"

    paginate_by = 15

    def get_queryset(self):

        queryset = (
            NewsArticle.objects
            .select_related("category")
            .order_by(
                "-published_at",
                "-created_at",
            )
        )

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        content_type = self.request.GET.get(
            "content_type",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(excerpt__icontains=search)
                | Q(content__icontains=search)
            )

        if status == "published":

            queryset = queryset.filter(
                published=True
            )

        elif status == "draft":

            queryset = queryset.filter(
                published=False
            )

        if content_type:

            queryset = queryset.filter(
                content_type=content_type
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["total_articles"] = (
            NewsArticle.objects.count()
        )

        context["published_articles"] = (
            NewsArticle.objects.filter(
                published=True
            ).count()
        )

        context["draft_articles"] = (
            NewsArticle.objects.filter(
                published=False
            ).count()
        )

        context["current_search"] = (
            self.request.GET.get("q", "")
        )

        context["current_status"] = (
            self.request.GET.get("status", "")
        )

        context["current_content_type"] = (
            self.request.GET.get(
                "content_type",
                ""
            )
        )

        context["content_types"] = (
            NewsArticle.ContentType.choices
        )

        return context


# =========================================================
# CREATE NEWS
# =========================================================

class DashboardNewsCreateView(
    NewsManagerRequiredMixin,
    CreateView
):

    model = NewsArticle

    form_class = NewsArticleForm

    template_name = "dashboard/news/form.html"

    success_url = reverse_lazy(
        "dashboard:news_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "News article created successfully."
        )

        return response


# =========================================================
# UPDATE NEWS
# =========================================================

class DashboardNewsUpdateView(
    NewsManagerRequiredMixin,
    UpdateView
):

    model = NewsArticle

    form_class = NewsArticleForm

    template_name = "dashboard/news/form.html"

    success_url = reverse_lazy(
        "dashboard:news_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "News article updated successfully."
        )

        return response


# =========================================================
# DELETE NEWS
# =========================================================

class DashboardNewsDeleteView(
    NewsManagerRequiredMixin,
    DeleteView
):

    model = NewsArticle

    template_name = "dashboard/news/delete.html"

    success_url = reverse_lazy(
        "dashboard:news_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "News article deleted successfully."
        )

        return super().form_valid(form)


# =========================================================
# EVENTS LIST
# =========================================================

class DashboardEventListView(
    EventsManagerRequiredMixin,
    ListView
):

    model = Event

    template_name = "dashboard/events/list.html"

    context_object_name = "events"

    paginate_by = 15

    def get_queryset(self):

        queryset = (
            Event.objects
            .order_by(
                "event_date",
                "start_time",
                "-created_at",
            )
        )

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        published = self.request.GET.get(
            "published",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(short_description__icontains=search)
                | Q(description__icontains=search)
                | Q(venue__icontains=search)
                | Q(location__icontains=search)
            )

        if status:

            queryset = queryset.filter(
                status=status
            )

        if published == "yes":

            queryset = queryset.filter(
                published=True
            )

        elif published == "no":

            queryset = queryset.filter(
                published=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["total_events"] = (
            Event.objects.count()
        )

        context["upcoming_events_count"] = (
            Event.objects.filter(
                status=Event.Status.UPCOMING
            ).count()
        )

        context["ongoing_events_count"] = (
            Event.objects.filter(
                status=Event.Status.ONGOING
            ).count()
        )

        context["completed_events_count"] = (
            Event.objects.filter(
                status=Event.Status.COMPLETED
            ).count()
        )

        context["cancelled_events_count"] = (
            Event.objects.filter(
                status=Event.Status.CANCELLED
            ).count()
        )

        context["published_events_count"] = (
            Event.objects.filter(
                published=True
            ).count()
        )

        context["current_search"] = (
            self.request.GET.get("q", "")
        )

        context["current_status"] = (
            self.request.GET.get("status", "")
        )

        context["current_published"] = (
            self.request.GET.get(
                "published",
                ""
            )
        )

        context["event_statuses"] = (
            Event.Status.choices
        )

        return context

# =========================================================
# CREATE EVENT
# =========================================================

class DashboardEventCreateView(
    EventsManagerRequiredMixin,
    CreateView
):

    model = Event

    form_class = EventForm

    template_name = "dashboard/events/form.html"

    success_url = reverse_lazy(
        "dashboard:event_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Event created successfully."
        )

        return response

# =========================================================
# UPDATE EVENT
# =========================================================

class DashboardEventUpdateView(
    EventsManagerRequiredMixin,
    UpdateView
):

    model = Event

    form_class = EventForm

    template_name = "dashboard/events/form.html"

    success_url = reverse_lazy(
        "dashboard:event_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Event updated successfully."
        )

        return response

# =========================================================
# DELETE EVENT
# =========================================================

class DashboardEventDeleteView(
    EventsManagerRequiredMixin,
    DeleteView
):

    model = Event

    template_name = "dashboard/events/delete.html"

    success_url = reverse_lazy(
        "dashboard:event_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Event deleted successfully."
        )

        return super().form_valid(form)


# ============================================================
# MEDIA ALBUM LIST
# ============================================================

class DashboardMediaAlbumListView(StaffRequiredMixin, ListView):

    model = MediaAlbum
    template_name = "dashboard/media/albums/list.html"
    context_object_name = "albums"
    paginate_by = 15

    def get_queryset(self):

        queryset = (
            MediaAlbum.objects
            .prefetch_related("images")
            .all()
        )

        search = self.request.GET.get("q", "").strip()
        published = self.request.GET.get("published", "")
        featured = self.request.GET.get("featured", "")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(location__icontains=search)
            )

        if published == "yes":
            queryset = queryset.filter(published=True)

        elif published == "no":
            queryset = queryset.filter(published=False)

        if featured == "yes":
            queryset = queryset.filter(featured=True)

        elif featured == "no":
            queryset = queryset.filter(featured=False)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_albums"] = MediaAlbum.objects.count()

        context["published_albums"] = (
            MediaAlbum.objects
            .filter(published=True)
            .count()
        )

        context["featured_albums"] = (
            MediaAlbum.objects
            .filter(featured=True)
            .count()
        )

        context["total_images"] = MediaImage.objects.count()

        context["search_query"] = (
            self.request.GET.get("q", "")
        )

        context["published_filter"] = (
            self.request.GET.get("published", "")
        )

        context["featured_filter"] = (
            self.request.GET.get("featured", "")
        )

        return context

# ============================================================
# CREATE ALBUM
# ============================================================

class DashboardMediaAlbumCreateView(
    StaffRequiredMixin,
    CreateView
):

    model = MediaAlbum
    form_class = MediaAlbumForm
    template_name = "dashboard/media/albums/form.html"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:media_album_images",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Media album created successfully."
        )

        return super().form_valid(form)


# ============================================================
# UPDATE ALBUM
# ============================================================

class DashboardMediaAlbumUpdateView(
    StaffRequiredMixin,
    UpdateView
):

    model = MediaAlbum
    form_class = MediaAlbumForm
    template_name = "dashboard/media/albums/form.html"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:media_album_images",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Media album updated successfully."
        )

        return super().form_valid(form)


# ============================================================
# DELETE ALBUM
# ============================================================

class DashboardMediaAlbumDeleteView(
    StaffRequiredMixin,
    DeleteView
):

    model = MediaAlbum
    template_name = "dashboard/media/albums/delete.html"
    success_url = reverse_lazy(
        "dashboard:media_album_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Media album deleted successfully."
        )

        return super().form_valid(form)

# ============================================================
# ALBUM IMAGE MANAGEMENT
# ============================================================

class DashboardMediaAlbumImagesView(
    StaffRequiredMixin,
    View
):

    template_name = "dashboard/media/albums/images.html"

    def get(self, request, pk):

        album = get_object_or_404(
            MediaAlbum,
            pk=pk
        )

        images = album.images.all()

        return render(
            request,
            self.template_name,
            {
                "album": album,
                "images": images,
                "image_count": images.count(),
            }
        )

# ============================================================
# ADD IMAGE TO ALBUM
# ============================================================

class DashboardMediaImageCreateView(
    StaffRequiredMixin,
    CreateView
):

    model = MediaImage
    form_class = MediaImageForm
    template_name = "dashboard/media/images/form.html"

    def dispatch(self, request, *args, **kwargs):

        self.album = MediaAlbum.objects.get(
            pk=kwargs["pk"]
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        form.instance.album = self.album

        messages.success(
            self.request,
            "Image added to album successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "dashboard:media_album_images",
            kwargs={"pk": self.album.pk}
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["album"] = self.album

        return context

# ============================================================
# DELETE IMAGE
# ============================================================

class DashboardMediaImageDeleteView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        image = get_object_or_404(
            MediaImage,
            pk=pk
        )

        album = image.album

        was_cover = (
            album.cover_image_source_id == image.pk
        )

        with transaction.atomic():

            image.delete()

            if was_cover:

                replacement = (
                    album.images
                    .order_by(
                        "display_order",
                        "created_at"
                    )
                    .first()
                )

                if replacement:

                    try:

                        with replacement.image.open(
                            "rb"
                        ) as image_file:

                            filename = (
                                f"album-{album.pk}-cover-"
                                f"{replacement.pk}-"
                                f"{replacement.image.name.split('/')[-1]}"
                            )

                            album.cover_image.save(
                                filename,
                                File(image_file),
                                save=False
                            )

                        album.cover_image_source = replacement

                    except Exception:

                        album.cover_image = None
                        album.cover_image_source = None

                else:

                    album.cover_image = None
                    album.cover_image_source = None

                album.save(
                    update_fields=[
                        "cover_image",
                        "cover_image_source",
                        "updated_at",
                    ]
                )

        messages.success(
            request,
            "Image deleted successfully."
        )

        return redirect(
            "dashboard:media_album_images",
            pk=album.pk
        )
# ============================================================
# MEDIA VIDEO LIST
# ============================================================

class DashboardMediaVideoListView(
    StaffRequiredMixin,
    ListView
):

    model = MediaVideo

    template_name = "dashboard/media/videos/list.html"

    context_object_name = "videos"

    paginate_by = 15

    def get_queryset(self):

        queryset = (
            MediaVideo.objects
            .all()
            .order_by(
                "display_order",
                "-published_at",
                "-created_at",
            )
        )

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        published = self.request.GET.get(
            "published",
            ""
        )

        featured = self.request.GET.get(
            "featured",
            ""
        )

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                |
                Q(description__icontains=search)
            )

        if published == "yes":

            queryset = queryset.filter(
                published=True
            )

        elif published == "no":

            queryset = queryset.filter(
                published=False
            )

        if featured == "yes":

            queryset = queryset.filter(
                featured=True
            )

        elif featured == "no":

            queryset = queryset.filter(
                featured=False
            )

        return queryset

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["total_videos"] = (
            MediaVideo.objects.count()
        )

        context["published_videos"] = (
            MediaVideo.objects
            .filter(
                published=True
            )
            .count()
        )

        context["featured_videos"] = (
            MediaVideo.objects
            .filter(
                featured=True
            )
            .count()
        )

        context["total_views"] = (
            sum(
                MediaVideo.objects.values_list(
                    "views",
                    flat=True
                )
            )
        )

        context["search_query"] = (
            self.request.GET.get(
                "q",
                ""
            )
        )

        context["published_filter"] = (
            self.request.GET.get(
                "published",
                ""
            )
        )

        context["featured_filter"] = (
            self.request.GET.get(
                "featured",
                ""
            )
        )

        return context

# ============================================================
# CREATE VIDEO
# ============================================================

class DashboardMediaVideoCreateView(
    StaffRequiredMixin,
    CreateView
):

    model = MediaVideo
    form_class = MediaVideoForm
    template_name = "dashboard/media/videos/form.html"
    success_url = reverse_lazy(
        "dashboard:media_video_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Video added successfully."
        )

        return super().form_valid(form)

# ============================================================
# UPDATE VIDEO
# ============================================================

class DashboardMediaVideoUpdateView(
    StaffRequiredMixin,
    UpdateView
):

    model = MediaVideo
    form_class = MediaVideoForm
    template_name = "dashboard/media/videos/form.html"
    success_url = reverse_lazy(
        "dashboard:media_video_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Video updated successfully."
        )

        return super().form_valid(form)
    
# ============================================================
# DELETE VIDEO
# ============================================================

class DashboardMediaVideoDeleteView(
    StaffRequiredMixin,
    DeleteView
):

    model = MediaVideo
    template_name = "dashboard/media/videos/delete.html"
    success_url = reverse_lazy(
        "dashboard:media_video_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Video deleted successfully."
        )

        return super().form_valid(form)

class DashboardMediaVideoReorderView(
    StaffRequiredMixin,
    View
):

    def post(self, request):

        try:

            data = json.loads(request.body)

            video_ids = data.get(
                "video_ids",
                []
            )

            if not isinstance(video_ids, list):

                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid video order."
                    },
                    status=400
                )


            videos = MediaVideo.objects.filter(
                pk__in=video_ids
            )


            video_map = {
                str(video.pk): video
                for video in videos
            }


            for index, video_id in enumerate(
                video_ids,
                start=1
            ):

                video = video_map.get(
                    str(video_id)
                )

                if video:

                    video.display_order = index

                    video.save(
                        update_fields=[
                            "display_order"
                        ]
                    )


            return JsonResponse(
                {
                    "success": True,
                    "message": "Video order saved successfully."
                }
            )


        except Exception:

            return JsonResponse(
                {
                    "success": False,
                    "message": "Unable to save video order."
                },
                status=400
            )

class DashboardMediaVideoTogglePublishedView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        video = get_object_or_404(
            MediaVideo,
            pk=pk
        )

        video.published = not video.published

        video.save(
            update_fields=[
                "published",
                "updated_at",
            ]
        )

        if video.published:

            messages.success(
                request,
                f'"{video.title}" has been published.'
            )

        else:

            messages.success(
                request,
                f'"{video.title}" has been unpublished.'
            )

        return redirect(
            "dashboard:media_video_list"
        )


class DashboardMediaVideoToggleFeaturedView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        video = get_object_or_404(
            MediaVideo,
            pk=pk
        )

        video.featured = not video.featured

        video.save(
            update_fields=[
                "featured",
                "updated_at",
            ]
        )

        if video.featured:

            messages.success(
                request,
                f'"{video.title}" is now featured.'
            )

        else:

            messages.success(
                request,
                f'"{video.title}" has been removed from featured videos.'
            )

        return redirect(
            "dashboard:media_video_list"
        )


class DashboardMediaBulkImageUploadView(StaffRequiredMixin, View):

    template_name = "dashboard/media/images/bulk_upload.html"

    def get(self, request, pk):

        album = get_object_or_404(
            MediaAlbum,
            pk=pk
        )

        form = MediaBulkImageUploadForm()

        return render(
            request,
            self.template_name,
            {
                "album": album,
                "form": form,
            }
        )

    def post(self, request, pk):

        album = get_object_or_404(
            MediaAlbum,
            pk=pk
        )

        form = MediaBulkImageUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            images = form.cleaned_data["images"]

            current_count = album.images.count()

            for index, uploaded_file in enumerate(
                images,
                start=1
            ):

                media_image = MediaImage.objects.create(
                    album=album,
                    image=uploaded_file,
                    display_order=current_count + index,
                    alt_text=album.title,
                )

                if not album.cover_image:

                    try:

                        with media_image.image.open(
                            "rb"
                        ) as image_file:

                            filename = (
                                f"album-{album.pk}-cover-"
                                f"{media_image.pk}-"
                                f"{media_image.image.name.split('/')[-1]}"
                            )

                            album.cover_image.save(
                                filename,
                                File(image_file),
                                save=False
                            )

                        album.cover_image_source = media_image

                        album.save(
                            update_fields=[
                                "cover_image",
                                "cover_image_source",
                                "updated_at",
                            ]
                        )

                    except Exception:

                        pass

            messages.success(
                request,
                f"{len(images)} image(s) uploaded successfully."
            )

            return redirect(
                "dashboard:media_album_images",
                pk=album.pk
            )
        return render(
            request,
            self.template_name,
            {
                "album": album,
                "form": form,
            }
        )


class DashboardMediaImageUpdateView(
    StaffRequiredMixin,
    View
):

    template_name = "dashboard/media/images/form.html"

    def get(self, request, pk):

        image = get_object_or_404(
            MediaImage,
            pk=pk
        )

        form = MediaImageForm(
            instance=image
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "image": image,
                "album": image.album,
                "is_edit": True,
            }
        )

    def post(self, request, pk):

        image = get_object_or_404(
            MediaImage,
            pk=pk
        )

        form = MediaImageForm(
            request.POST,
            request.FILES,
            instance=image
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Image updated successfully."
            )

            return redirect(
                "dashboard:media_album_images",
                pk=image.album.pk
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "image": image,
                "album": image.album,
                "is_edit": True,
            }
        )

class DashboardMediaImageReorderView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        album = get_object_or_404(
            MediaAlbum,
            pk=pk
        )

        try:

            data = json.loads(
                request.body
            )

            image_ids = data.get(
                "image_ids",
                []
            )

            if not isinstance(
                image_ids,
                list
            ):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid image order."
                    },
                    status=400
                )

            images = MediaImage.objects.filter(
                album=album,
                pk__in=image_ids
            )

            image_map = {
                str(image.pk): image
                for image in images
            }

            for index, image_id in enumerate(
                image_ids,
                start=1
            ):

                image = image_map.get(
                    str(image_id)
                )

                if image:

                    image.display_order = index

                    image.save(
                        update_fields=[
                            "display_order"
                        ]
                    )

            return JsonResponse(
                {
                    "success": True,
                    "message": "Image order saved successfully."
                }
            )

        except Exception:

            return JsonResponse(
                {
                    "success": False,
                    "message": "Unable to save image order."
                },
                status=400
            )


class DashboardMediaImageSetCoverView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        image = get_object_or_404(
            MediaImage,
            pk=pk
        )

        album = image.album

        if not image.image:
            messages.error(
                request,
                "This image cannot be used as a cover image."
            )

            return redirect(
                "dashboard:media_album_images",
                pk=album.pk
            )

        try:

            with image.image.open("rb") as image_file:

                filename = (
                    f"album-{album.pk}-cover-"
                    f"{image.pk}-"
                    f"{image.image.name.split('/')[-1]}"
                )

                album.cover_image.save(
                    filename,
                    File(image_file),
                    save=False
                )

            album.cover_image_source = image

            album.save(
                update_fields=[
                    "cover_image",
                    "cover_image_source",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                f'"{image.caption or "Image"}" is now the album cover.'
            )

        except Exception:

            messages.error(
                request,
                "Unable to set this image as the album cover."
            )

        return redirect(
            "dashboard:media_album_images",
            pk=album.pk
        )

class DashboardMediaBulkImageDeleteView(
    StaffRequiredMixin,
    View
):

    def post(self, request, pk):

        album = get_object_or_404(
            MediaAlbum,
            pk=pk
        )

        image_ids = request.POST.getlist(
            "image_ids"
        )

        if not image_ids:
            messages.warning(
                request,
                "Please select at least one image."
            )

            return redirect(
                "dashboard:media_album_images",
                pk=album.pk
            )

        images = MediaImage.objects.filter(
            album=album,
            pk__in=image_ids
        )

        if not images.exists():
            messages.warning(
                request,
                "No valid images were selected."
            )

            return redirect(
                "dashboard:media_album_images",
                pk=album.pk
            )

        image_count = images.count()

        # Check whether the current album cover
        # is among the images being deleted.
        cover_was_deleted = False

        if album.cover_image:

            cover_name = album.cover_image.name

            cover_was_deleted = images.filter(
                image=cover_name
            ).exists()

        with transaction.atomic():

            images.delete()

            # If the album cover was deleted,
            # automatically choose another image.
            if cover_was_deleted:

                replacement = album.images.order_by(
                    "display_order",
                    "created_at"
                ).first()

                if replacement and replacement.image:

                    album.cover_image = replacement.image

                else:

                    album.cover_image = None

                album.save(
                    update_fields=[
                        "cover_image",
                        "updated_at",
                    ]
                )

            # Normalize remaining image order.
            remaining_images = album.images.order_by(
                "display_order",
                "created_at"
            )

            for index, image in enumerate(
                remaining_images,
                start=1
            ):

                if image.display_order != index:

                    image.display_order = index

                    image.save(
                        update_fields=[
                            "display_order"
                        ]
                    )

        messages.success(
            request,
            f"{image_count} image(s) deleted successfully."
        )

        return redirect(
            "dashboard:media_album_images",
            pk=album.pk
        )

# =========================================================
# AGENDA MANAGEMENT
# =========================================================

class DashboardAgendaListView(
    StaffRequiredMixin,
    ListView
):

    model = Agenda

    template_name = "dashboard/agenda/list.html"

    context_object_name = "agendas"

    paginate_by = 20

    def get_queryset(self):

        queryset = Agenda.objects.all().order_by(
            "number",
            "title"
        )

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        if status == "active":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "inactive":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["total_agendas"] = (
            Agenda.objects.count()
        )

        context["active_agendas"] = (
            Agenda.objects.filter(
                is_active=True
            ).count()
        )

        context["inactive_agendas"] = (
            Agenda.objects.filter(
                is_active=False
            ).count()
        )

        context["current_search"] = (
            self.request.GET.get("q", "")
        )

        context["current_status"] = (
            self.request.GET.get("status", "")
        )

        return context


# =========================================================
# CREATE AGENDA
# =========================================================

class DashboardAgendaCreateView(
    StaffRequiredMixin,
    CreateView
):

    model = Agenda

    fields = [
        "number",
        "title",
        "description",
        "icon",
        "is_active",
    ]

    template_name = "dashboard/agenda/form.html"

    success_url = reverse_lazy(
        "dashboard:agenda_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Agenda item created successfully."
        )

        return response


# =========================================================
# UPDATE AGENDA
# =========================================================

class DashboardAgendaUpdateView(
    StaffRequiredMixin,
    UpdateView
):

    model = Agenda

    fields = [
        "number",
        "title",
        "description",
        "icon",
        "is_active",
    ]

    template_name = "dashboard/agenda/form.html"

    success_url = reverse_lazy(
        "dashboard:agenda_list"
    )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Agenda item updated successfully."
        )

        return response


# =========================================================
# DELETE AGENDA
# =========================================================

class DashboardAgendaDeleteView(
    StaffRequiredMixin,
    DeleteView
):

    model = Agenda

    template_name = "dashboard/agenda/delete.html"

    success_url = reverse_lazy(
        "dashboard:agenda_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Agenda item deleted successfully."
        )

        return super().form_valid(form)

    