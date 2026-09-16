from django.urls import path

from django.urls import path

from .views import (
    # Public media
    AlbumListView,
    AlbumDetailView,
    VideoListView,
    VideoDetailView,

    # Dashboard
    MediaDashboardView,

    MediaAlbumListView,
    MediaAlbumCreateView,
    MediaAlbumUpdateView,
    MediaAlbumManageView,
    MediaAlbumDeleteView,
    MediaBulkImageUploadView,

    MediaImageUpdateView,
    MediaImageDeleteView,

    MediaVideoListView,
    MediaVideoCreateView,
    MediaVideoManageView,
    MediaVideoUpdateView,
    MediaVideoDeleteView,
)


app_name = "media"


urlpatterns = [

    # =========================================================
    # PUBLIC MEDIA
    # =========================================================

    path(
        "gallery/",
        AlbumListView.as_view(),
        name="gallery",
    ),

    path(
        "gallery/<slug:slug>/",
        AlbumDetailView.as_view(),
        name="album_detail",
    ),

    path(
        "videos/",
        VideoListView.as_view(),
        name="videos",
    ),

    path(
        "videos/<slug:slug>/",
        VideoDetailView.as_view(),
        name="video_detail",
    ),


    # =========================================================
    # MEDIA DASHBOARD
    # =========================================================

    path(
        "dashboard/",
        MediaDashboardView.as_view(),
        name="dashboard",
    ),


    # =========================================================
    # ALBUM MANAGEMENT
    # =========================================================

    path(
        "dashboard/albums/",
        MediaAlbumListView.as_view(),
        name="album_list",
    ),

    path(
        "dashboard/albums/create/",
        MediaAlbumCreateView.as_view(),
        name="album_create",
    ),

    path(
        "dashboard/albums/<int:pk>/",
        MediaAlbumManageView.as_view(),
        name="album_manage",
    ),

    path(
        "dashboard/albums/<int:pk>/edit/",
        MediaAlbumUpdateView.as_view(),
        name="album_edit",
    ),

    path(
        "dashboard/albums/<int:pk>/delete/",
        MediaAlbumDeleteView.as_view(),
        name="album_delete",
    ),

    path(
        "dashboard/albums/<int:pk>/upload/",
        MediaBulkImageUploadView.as_view(),
        name="image_upload",
    ),


    # =========================================================
    # IMAGE MANAGEMENT
    # =========================================================

    path(
        "dashboard/images/<int:pk>/edit/",
        MediaImageUpdateView.as_view(),
        name="image_edit",
    ),

    path(
        "dashboard/images/<int:pk>/delete/",
        MediaImageDeleteView.as_view(),
        name="image_delete",
    ),


    # =========================================================
    # VIDEO MANAGEMENT
    # =========================================================

    path(
        "dashboard/videos/",
        MediaVideoListView.as_view(),
        name="video_manage",
    ),

    path(
        "dashboard/videos/create/",
        MediaVideoCreateView.as_view(),
        name="video_create",
    ),

    path(
        "dashboard/videos/<int:pk>/",
        MediaVideoManageView.as_view(),
        name="video_detail_manage",
    ),

    path(
        "dashboard/videos/<int:pk>/edit/",
        MediaVideoUpdateView.as_view(),
        name="video_edit",
    ),

    path(
        "dashboard/videos/<int:pk>/delete/",
        MediaVideoDeleteView.as_view(),
        name="video_delete",
    ),

]
