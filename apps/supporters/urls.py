from django.urls import path

from .views import (
    join,
    SupporterSuccessView,
    SupporterDashboardView,
    SupporterDetailView,
    SupporterStatusUpdateView,
    SupporterEditView,
)


app_name = "supporters"


urlpatterns = [

    # Public registration
    path(
        "",
        join,
        name="join",
    ),

    path(
        "success/",
        SupporterSuccessView.as_view(),
        name="success",
    ),

    # Admin dashboard
    path(
        "dashboard/",
        SupporterDashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "<int:pk>/edit/",
        SupporterEditView.as_view(),
        name="edit",
    ),

    path(
        "dashboard/<int:pk>/",
        SupporterDetailView.as_view(),
        name="detail",
    ),

    path(
        "dashboard/<int:pk>/status/",
        SupporterStatusUpdateView.as_view(),
        name="status_update",
    ),

]