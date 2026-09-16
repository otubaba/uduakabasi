from django.urls import path

from .views import (
    ApplicationCreateView,
    ApplicationSuccessView,
    ProgrammeDetailView,
    ProgrammeListView,
    polling_units_ajax,
    wards_ajax,
    EmpowermentDashboardView,
    EmpowermentApplicationListView,
    EmpowermentApplicationDetailView,
    EmpowermentApplicationStatusUpdateView,
    EmpowermentApplicationReviewView,
)


app_name = "empowerment"


urlpatterns = [

    path(
        "",
        ProgrammeListView.as_view(),
        name="programmes",
    ),
    path(
        "dashboard/",
        EmpowermentDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "ajax/wards/",
        wards_ajax,
        name="wards_ajax",
    ),

    path(
        "ajax/polling-units/",
        polling_units_ajax,
        name="polling_units_ajax",
    ),

    path(
        "application/success/<str:application_number>/",
        ApplicationSuccessView.as_view(),
        name="application_success",
    ),

    path(
        "<slug:slug>/apply/",
        ApplicationCreateView.as_view(),
        name="apply",
    ),

    path(
        "dashboard/applications/",
        EmpowermentApplicationListView.as_view(),
        name="application_list",
    ),
    path(
        "dashboard/applications/<int:pk>/",
        EmpowermentApplicationDetailView.as_view(),
        name="application_detail",
    ),
    path(
        "dashboard/applications/<int:pk>/status/",
        EmpowermentApplicationStatusUpdateView.as_view(),
        name="application_status_update",
    ),
    path(
        "dashboard/applications/<int:pk>/review/",
        EmpowermentApplicationReviewView.as_view(),
        name="application_review",
    ),

    path(
        "<slug:slug>/",
        ProgrammeDetailView.as_view(),
        name="programme_detail",
    ),
    
]