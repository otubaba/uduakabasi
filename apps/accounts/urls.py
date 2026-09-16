from django.urls import path

from .views import (
    StaffLoginView,
    StaffLogoutView,
    StaffCreateView,
    StaffListView,
    StaffEditView,
    StaffToggleStatusView,
    StaffPasswordResetView,
)

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        StaffLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        StaffLogoutView.as_view(),
        name="logout",
    ),

    path(
        "staff/create/",
        StaffCreateView.as_view(),
        name="staff_create",
    ),
    path(
        "staff/",
        StaffListView.as_view(),
        name="staff_list",
    ),
    path(
        "staff/<int:pk>/edit/",
        StaffEditView.as_view(),
        name="staff_edit",
    ),
    path(
        "staff/<int:pk>/toggle-status/",
        StaffToggleStatusView.as_view(),
        name="staff_toggle_status",
    ),
    path(
        "staff/<int:pk>/password-reset/",
        StaffPasswordResetView.as_view(),
        name="staff_password_reset",
    ),
]