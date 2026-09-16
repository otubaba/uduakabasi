from django.urls import path

from .views import (
    DashboardHomeView,
    DashboardNewsListView,
    DashboardNewsCreateView,
    DashboardNewsUpdateView,
    DashboardNewsDeleteView,

    DashboardEventListView,
    DashboardEventCreateView,
    DashboardEventUpdateView,
    DashboardEventDeleteView,

    DashboardMediaAlbumListView,
    DashboardMediaAlbumCreateView,
    DashboardMediaAlbumUpdateView,
    DashboardMediaAlbumDeleteView,
    DashboardMediaAlbumImagesView,
    DashboardMediaImageCreateView,
    DashboardMediaImageDeleteView,
    DashboardMediaImageSetCoverView,

    DashboardMediaVideoListView,
    DashboardMediaVideoCreateView,
    DashboardMediaVideoUpdateView,
    DashboardMediaVideoDeleteView,
    DashboardMediaBulkImageUploadView,
    DashboardMediaImageReorderView,
    DashboardMediaImageUpdateView,
    DashboardMediaBulkImageDeleteView,

    DashboardMediaVideoTogglePublishedView,
    DashboardMediaVideoToggleFeaturedView,
    DashboardMediaVideoReorderView,

    DashboardAgendaListView,
    DashboardAgendaCreateView,
    DashboardAgendaUpdateView,
    DashboardAgendaDeleteView,
    
)


app_name = "dashboard"


urlpatterns = [

    # =====================================================
    # DASHBOARD HOME
    # =====================================================

    path(
        "",
        DashboardHomeView.as_view(),
        name="home",
    ),


    # =====================================================
    # NEWS MANAGEMENT
    # =====================================================

    path(
        "news/",
        DashboardNewsListView.as_view(),
        name="news_list",
    ),

    path(
        "news/create/",
        DashboardNewsCreateView.as_view(),
        name="news_create",
    ),

    path(
        "news/<int:pk>/edit/",
        DashboardNewsUpdateView.as_view(),
        name="news_edit",
    ),

    path(
        "news/<int:pk>/delete/",
        DashboardNewsDeleteView.as_view(),
        name="news_delete",
    ),

    # =====================================================
    # EVENTS MANAGEMENT
    # =====================================================

    path(
        "events/",
        DashboardEventListView.as_view(),
        name="event_list",
    ),

    path(
        "events/create/",
        DashboardEventCreateView.as_view(),
        name="event_create",
    ),

    path(
        "events/<int:pk>/edit/",
        DashboardEventUpdateView.as_view(),
        name="event_edit",
    ),

    path(
        "events/<int:pk>/delete/",
        DashboardEventDeleteView.as_view(),
        name="event_delete",
    ),

    # ============================================================
    # MEDIA / GALLERY
    # ============================================================

    path(
        "media/",
        DashboardMediaAlbumListView.as_view(),
        name="media_album_list",
    ),

    path(
        "media/albums/create/",
        DashboardMediaAlbumCreateView.as_view(),
        name="media_album_create",
    ),

    path(
        "media/albums/<int:pk>/edit/",
        DashboardMediaAlbumUpdateView.as_view(),
        name="media_album_edit",
    ),

    path(
        "media/albums/<int:pk>/delete/",
        DashboardMediaAlbumDeleteView.as_view(),
        name="media_album_delete",
    ),

    path(
        "media/albums/<int:pk>/images/",
        DashboardMediaAlbumImagesView.as_view(),
        name="media_album_images",
    ),

    path(
        "media/albums/<int:pk>/images/add/",
        DashboardMediaImageCreateView.as_view(),
        name="media_image_create",
    ),

    path(
        "media/images/<int:pk>/delete/",
        DashboardMediaImageDeleteView.as_view(),
        name="media_image_delete",
    ),
    path(
        "media/images/<int:pk>/set-cover/",
        DashboardMediaImageSetCoverView.as_view(),
        name="media_image_set_cover",
    ),


    # ============================================================
    # MEDIA VIDEOS
    # ============================================================

    path(
        "media/videos/",
        DashboardMediaVideoListView.as_view(),
        name="media_video_list",
    ),

    path(
        "media/videos/create/",
        DashboardMediaVideoCreateView.as_view(),
        name="media_video_create",
    ),

    path(
        "media/videos/<int:pk>/edit/",
        DashboardMediaVideoUpdateView.as_view(),
        name="media_video_edit",
    ),

    path(
        "media/videos/<int:pk>/delete/",
        DashboardMediaVideoDeleteView.as_view(),
        name="media_video_delete",
    ),

    path(
        "media/albums/<int:pk>/images/bulk-upload/",
        DashboardMediaBulkImageUploadView.as_view(),
        name="media_bulk_image_upload",
    ),
    path(
    "media/",
    DashboardMediaAlbumListView.as_view(),
    name="media_album_list",
    ),

    path(
        "media/albums/create/",
        DashboardMediaAlbumCreateView.as_view(),
        name="media_album_create",
    ),

    path(
        "media/albums/<int:pk>/edit/",
        DashboardMediaAlbumUpdateView.as_view(),
        name="media_album_edit",
    ),

    path(
        "media/albums/<int:pk>/delete/",
        DashboardMediaAlbumDeleteView.as_view(),
        name="media_album_delete",
    ),

    path(
        "media/albums/<int:pk>/images/",
        DashboardMediaAlbumImagesView.as_view(),
        name="media_album_images",
    ),

    path(
        "media/albums/<int:pk>/images/add/",
        DashboardMediaImageCreateView.as_view(),
        name="media_image_create",
    ),

    path(
        "media/albums/<int:pk>/images/bulk-upload/",
        DashboardMediaBulkImageUploadView.as_view(),
        name="media_bulk_image_upload",
    ),

    path(
        "media/albums/<int:pk>/images/bulk-delete/",
        DashboardMediaBulkImageDeleteView.as_view(),
        name="media_bulk_image_delete",
    ),

    path(
        "media/images/<int:pk>/edit/",
        DashboardMediaImageUpdateView.as_view(),
        name="media_image_edit",
    ),

    path(
        "media/images/<int:pk>/set-cover/",
        DashboardMediaImageSetCoverView.as_view(),
        name="media_image_set_cover",
    ),

    path(
        "media/images/<int:pk>/delete/",
        DashboardMediaImageDeleteView.as_view(),
        name="media_image_delete",
    ),

    path(
        "media/albums/<int:pk>/images/reorder/",
        DashboardMediaImageReorderView.as_view(),
        name="media_image_reorder",
    ),
    path(
        "media/videos/<int:pk>/toggle-published/",
        DashboardMediaVideoTogglePublishedView.as_view(),
        name="media_video_toggle_published",
    ),

    path(
        "media/videos/<int:pk>/toggle-featured/",
        DashboardMediaVideoToggleFeaturedView.as_view(),
        name="media_video_toggle_featured",
    ),
    path(
        "media/videos/reorder/",
        DashboardMediaVideoReorderView.as_view(),
        name="media_video_reorder",
    ),
    # =====================================================
    # AGENDA MANAGEMENT
    # =====================================================

    path(
        "agenda/",
        DashboardAgendaListView.as_view(),
        name="agenda_list",
    ),

    path(
        "agenda/create/",
        DashboardAgendaCreateView.as_view(),
        name="agenda_create",
    ),

    path(
        "agenda/<int:pk>/edit/",
        DashboardAgendaUpdateView.as_view(),
        name="agenda_edit",
    ),

    path(
        "agenda/<int:pk>/delete/",
        DashboardAgendaDeleteView.as_view(),
        name="agenda_delete",
    ),

]