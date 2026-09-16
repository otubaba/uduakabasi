from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.utils import timezone
from .forms import EmpowermentApplicationForm
from .models import (
    EmpowermentApplication,
    EmpowermentProgramme,
    LocalGovernment,
    Ward,
    PollingUnit,
)
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import EmpowermentApplication
from django.db.models import Count, Q

def wards_ajax(request):

    lga_id = request.GET.get("lga")

    if not lga_id:
        return JsonResponse(
            {
                "wards": []
            }
        )

    wards = (
        Ward.objects
        .filter(
            local_government_id=lga_id,
            active=True,
        )
        .order_by(
            "display_order",
            "name",
        )
    )

    data = [
        {
            "id": ward.id,
            "name": ward.name,
            "code": ward.code,
        }
        for ward in wards
    ]

    return JsonResponse(
        {
            "wards": data
        }
    )


def polling_units_ajax(request):

    ward_id = request.GET.get("ward")

    if not ward_id:
        return JsonResponse(
            {
                "polling_units": []
            }
        )

    polling_units = (
        PollingUnit.objects
        .filter(
            ward_id=ward_id,
            active=True,
        )
        .order_by(
            "display_order",
            "code",
        )
    )

    data = [
        {
            "id": polling_unit.id,
            "code": polling_unit.code,
            "name": polling_unit.name,
            "type": polling_unit.polling_unit_type,
            "label": (
                f"{polling_unit.code} — "
                f"{polling_unit.name}"
            ),
        }
        for polling_unit in polling_units
    ]

    return JsonResponse(
        {
            "polling_units": data
        }
    )


class ProgrammeListView(ListView):

    model = EmpowermentProgramme

    template_name = "empowerment/programmes.html"

    context_object_name = "programmes"

    paginate_by = 9

    def get_queryset(self):

        return (
            EmpowermentProgramme.objects
            .filter(
                published=True,
                active=True,
            )
            .order_by(
                "-featured",
                "-created_at",
            )
        )


class ProgrammeDetailView(DetailView):
    model = EmpowermentProgramme
    template_name = "empowerment/programme_detail.html"
    context_object_name = "programme"

    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return EmpowermentProgramme.objects.filter(
            published=True,
            active=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        programme = self.object
        now = timezone.now()

        application_count = (
            EmpowermentApplication.objects
            .filter(programme=programme)
            .exclude(status="withdrawn")
            .count()
        )

        # -----------------------------------------------
        # DETERMINE APPLICATION STATUS
        # -----------------------------------------------

        applications_open = True

        if (
            programme.application_start
            and now < programme.application_start
        ):
            applications_open = False

        if (
            programme.application_end
            and now > programme.application_end
        ):
            applications_open = False

        if (
            programme.maximum_applicants
            and application_count >= programme.maximum_applicants
        ):
            applications_open = False

        context["application_count"] = application_count
        context["applications_open"] = applications_open

        return context
    

class ApplicationCreateView(CreateView):
    model = EmpowermentApplication
    form_class = EmpowermentApplicationForm
    template_name = "empowerment/apply.html"

    def dispatch(self, request, *args, **kwargs):
        self.programme = (
            EmpowermentProgramme.objects
            .filter(
                slug=kwargs["slug"],
                published=True,
                active=True,
            )
            .first()
        )

        if not self.programme:
            messages.error(
                request,
                "This empowerment programme is currently unavailable."
            )
            return redirect("empowerment:programmes")

        now = timezone.now()

        # -------------------------------------------------
        # APPLICATION START DATE
        # -------------------------------------------------

        if (
            self.programme.application_start
            and now < self.programme.application_start
        ):
            messages.info(
                request,
                "Applications for this programme have not opened yet."
            )
            return redirect("empowerment:programme_detail",
                            slug=self.programme.slug)

        # -------------------------------------------------
        # APPLICATION END DATE
        # -------------------------------------------------

        if (
            self.programme.application_end
            and now > self.programme.application_end
        ):
            messages.warning(
                request,
                "Applications for this programme are now closed."
            )
            return redirect("empowerment:programme_detail",
                            slug=self.programme.slug)

        # -------------------------------------------------
        # MAXIMUM APPLICANTS
        # -------------------------------------------------

        if self.programme.maximum_applicants:

            application_count = (
                EmpowermentApplication.objects
                .filter(programme=self.programme)
                .exclude(status="withdrawn")
                .count()
            )

            if application_count >= self.programme.maximum_applicants:
                messages.warning(
                    request,
                    "The maximum number of applications for this programme has been reached."
                )
                return redirect(
                    "empowerment:programme_detail",
                    slug=self.programme.slug,
                )

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["programme"] = self.programme
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programme"] = self.programme
        return context

    def form_valid(self, form):
        form.instance.programme = self.programme
        form.instance.status = "submitted"

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Your empowerment application has been submitted successfully."
        )

        return response

    def get_success_url(self):
        return reverse(
            "empowerment:application_success",
            kwargs={
                "application_number": self.object.application_number
            },
        )


class ApplicationSuccessView(TemplateView):

    template_name = "empowerment/success.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        application_number = kwargs.get(
            "application_number"
        )

        context["application"] = (
            EmpowermentApplication.objects
            .filter(
                application_number=application_number
            )
            .select_related("programme")
            .first()
        )

        return context


class EmpowermentManagerRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin
):

    def test_func(self):
        return (
            self.request.user.is_active
            and (
                self.request.user.is_superuser
                or self.request.user.groups.filter(
                    name="Empowerment Manager"
                ).exists()
            )
        )

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(
            self.request,
            "You do not have permission to manage empowerment programmes."
        )

        return redirect("dashboard:home")



class EmpowermentDashboardView(
    EmpowermentManagerRequiredMixin,
    TemplateView
):
    template_name = "dashboard/empowerment/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        applications = EmpowermentApplication.objects.all()

        # ==========================================
        # APPLICATION STATISTICS
        # ==========================================

        context["total_applications"] = applications.count()

        context["submitted_applications"] = applications.filter(
            status="submitted"
        ).count()

        context["under_review_applications"] = applications.filter(
            status="under_review"
        ).count()

        context["approved_applications"] = applications.filter(
            status="approved"
        ).count()

        context["completed_applications"] = applications.filter(
            status="completed"
        ).count()

        context["shortlisted_applications"] = applications.filter(
            status="shortlisted"
        ).count()

        context["waitlisted_applications"] = applications.filter(
            status="waitlisted"
        ).count()

        context["not_selected_applications"] = applications.filter(
            status="not_selected"
        ).count()

        context["withdrawn_applications"] = applications.filter(
            status="withdrawn"
        ).count()

        # ==========================================
        # RECENT APPLICATIONS
        # ==========================================

        context["recent_applications"] = (
            applications
            .select_related(
                "programme",
                "local_government",
                "ward",
                "polling_unit",
            )
            .order_by("-created_at")[:10]
        )

        # ==========================================
        # APPLICATIONS BY LGA
        # ==========================================

        context["applications_by_lga"] = (
            applications
            .values("local_government__name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # ==========================================
        # APPLICATIONS BY PROGRAMME
        # ==========================================

        context["applications_by_programme"] = (
            applications
            .values("programme__title")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        # ==========================================
        # APPLICATIONS BY GENDER
        # ==========================================

        context["applications_by_gender"] = (
            applications
            .values("gender")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # ==========================================
        # APPLICATIONS BY EMPLOYMENT STATUS
        # ==========================================

        context["applications_by_employment"] = (
            applications
            .values("employment_status")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return context

class EmpowermentApplicationListView(
    EmpowermentManagerRequiredMixin,
    ListView
):
    model = EmpowermentApplication
    template_name = "dashboard/empowerment/applications/list.html"
    context_object_name = "applications"
    paginate_by = 20

    def get_queryset(self):

        queryset = (
            EmpowermentApplication.objects
            .select_related(
                "programme",
                "local_government",
                "ward",
                "polling_unit",
            )
            .order_by("-created_at")
        )

        # ==========================================
        # SEARCH
        # ==========================================

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(
                Q(application_number__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(other_names__icontains=search)
                | Q(phone__icontains=search)
                | Q(email__icontains=search)
            )

        # ==========================================
        # STATUS FILTER
        # ==========================================

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        if status:
            queryset = queryset.filter(
                status=status
            )

        # ==========================================
        # PROGRAMME FILTER
        # ==========================================

        programme = self.request.GET.get(
            "programme",
            ""
        ).strip()

        if programme:
            queryset = queryset.filter(
                programme_id=programme
            )

        # ==========================================
        # LGA FILTER
        # ==========================================

        local_government = self.request.GET.get(
            "local_government",
            ""
        ).strip()

        if local_government:
            queryset = queryset.filter(
                local_government_id=local_government
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["programmes"] = EmpowermentProgramme.objects.all().order_by(
            "title"
        )

        context["local_governments"] = (
            LocalGovernment.objects.all().order_by(
                "name"
            )
        )

        context["status_choices"] = [
            ("submitted", "Submitted"),
            ("under_review", "Under Review"),
            ("shortlisted", "Shortlisted"),
            ("approved", "Approved"),
            ("waitlisted", "Waitlisted"),
            ("not_selected", "Not Selected"),
            ("completed", "Completed"),
            ("withdrawn", "Withdrawn"),
        ]

        context["current_search"] = (
            self.request.GET.get("q", "")
        )

        context["current_status"] = (
            self.request.GET.get("status", "")
        )

        context["current_programme"] = (
            self.request.GET.get("programme", "")
        )

        context["current_local_government"] = (
            self.request.GET.get(
                "local_government",
                ""
            )
        )

        return context
    
class EmpowermentApplicationDetailView(
    EmpowermentManagerRequiredMixin,
    DetailView
):
    model = EmpowermentApplication
    template_name = "dashboard/empowerment/applications/detail.html"
    context_object_name = "application"

    def get_queryset(self):
        return (
            EmpowermentApplication.objects
            .select_related(
                "programme",
                "local_government",
                "ward",
                "polling_unit",
            )
        )

class EmpowermentApplicationStatusUpdateView(
    EmpowermentManagerRequiredMixin,
    View
):
    def post(self, request, pk):

        application = get_object_or_404(
            EmpowermentApplication,
            pk=pk
        )

        new_status = request.POST.get("status", "").strip()

        allowed_statuses = [
            "submitted",
            "under_review",
            "shortlisted",
            "approved",
            "waitlisted",
            "not_selected",
            "completed",
            "withdrawn",
        ]

        if new_status not in allowed_statuses:
            messages.error(
                request,
                "Invalid application status."
            )

            return redirect(
                "empowerment:application_detail",
                pk=application.pk
            )

        application.status = new_status

        if new_status != "submitted":
            application.reviewed_at = timezone.now()

            application.save(
                update_fields=[
                    "status",
                    "reviewed_at",
                    "updated_at",
                ]
            )
        else:
            application.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        messages.success(
            request,
            "Application status updated successfully."
        )

        return redirect(
            "empowerment:application_detail",
            pk=application.pk
        )

class EmpowermentApplicationReviewView(
    EmpowermentManagerRequiredMixin,
    View
):
    def post(self, request, pk):

        application = get_object_or_404(
            EmpowermentApplication,
            pk=pk
        )

        application.reviewer_notes = request.POST.get(
            "reviewer_notes",
            ""
        ).strip()

        application.reviewed_at = timezone.now()

        application.save(
            update_fields=[
                "reviewer_notes",
                "reviewed_at",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Review notes saved successfully."
        )

        return redirect(
            "empowerment:application_detail",
            pk=application.pk
        )

