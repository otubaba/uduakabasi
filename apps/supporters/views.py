from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    SupporterEditForm,
    SupporterRegistrationForm,
)
from .mixins import StaffRequiredMixin
from .models import Supporter


# =========================================================
# PUBLIC REGISTRATION
# =========================================================

def join(request):

    if request.method == "POST":

        form = SupporterRegistrationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Thank you for joining UDUAK-ABASI 2027."
            )

            return redirect(
                "supporters:success"
            )

    else:

        form = SupporterRegistrationForm()

    return render(
        request,
        "supporters/join.html",
        {
            "form": form,
        },
    )


class SupporterSuccessView(TemplateView):

    template_name = (
        "supporters/success.html"
    )

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class SupportersManagerRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin
):

    def test_func(self):

        return (
            self.request.user.is_active
            and (
                self.request.user.is_superuser
                or self.request.user.groups.filter(
                    name="Supporters Manager"
                ).exists()
            )
        )

    def handle_no_permission(self):

        messages.error(
            self.request,
            "You do not have permission to manage supporters."
        )

        return redirect(
            "dashboard:home"
        )

    
# =========================================================
# SUPPORTER DASHBOARD
# =========================================================

class SupporterDashboardView(
    SupportersManagerRequiredMixin,
    ListView
):

    model = Supporter

    template_name = (
        "supporters/dashboard.html"
    )

    context_object_name = "supporters"

    paginate_by = 20

    def get_queryset(self):

        queryset = Supporter.objects.all()

        search = self.request.GET.get(
            "q",
            ""
        ).strip()

        status = self.request.GET.get(
            "status",
            ""
        ).strip()

        lga = self.request.GET.get(
            "lga",
            ""
        ).strip()

        volunteer = self.request.GET.get(
            "volunteer",
            ""
        ).strip()

        if search:

            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(phone__icontains=search)
                | Q(email__icontains=search)
                | Q(community__icontains=search)
                | Q(ward__icontains=search)
            )

        if status:

            queryset = queryset.filter(
                status=status
            )

        if lga:

            queryset = queryset.filter(
                lga__iexact=lga
            )

        if volunteer == "yes":

            queryset = queryset.filter(
                volunteer=True
            )

        elif volunteer == "no":

            queryset = queryset.filter(
                volunteer=False
            )

        return queryset.order_by(
            "-registered_at"
        )

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

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
        context["contacted_supporters"] = (
            Supporter.objects.filter(
                status=Supporter.Status.CONTACTED
            ).count()
        )

        context["volunteer_count"] = (
            Supporter.objects.filter(
                volunteer=True
            ).count()
        )

        context["lgas"] = (
            Supporter.objects
            .exclude(lga="")
            .values_list(
                "lga",
                flat=True
            )
            .distinct()
            .order_by("lga")
        )

        context["current_search"] = (
            self.request.GET.get(
                "q",
                ""
            )
        )

        context["current_status"] = (
            self.request.GET.get(
                "status",
                ""
            )
        )

        context["current_lga"] = (
            self.request.GET.get(
                "lga",
                ""
            )
        )

        context["current_volunteer"] = (
            self.request.GET.get(
                "volunteer",
                ""
            )
        )

        return context




# =========================================================
# SUPPORTER DETAIL
# =========================================================

class SupporterDetailView(
    SupportersManagerRequiredMixin,
    DetailView
):

    model = Supporter

    template_name = (
        "supporters/detail.html"
    )

    context_object_name = "supporter"

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["status_choices"] = (
            Supporter.Status.choices
        )

        return context


# =========================================================
# SUPPORTER STATUS UPDATE
# =========================================================

class SupporterStatusUpdateView(
    SupportersManagerRequiredMixin,
    TemplateView
):

    def post(
        self,
        request,
        pk
    ):

        supporter = get_object_or_404(
            Supporter,
            pk=pk
        )

        status = request.POST.get(
            "status"
        )

        valid_statuses = {
            value
            for value, label
            in Supporter.Status.choices
        }

        if status not in valid_statuses:

            messages.error(
                request,
                "Invalid supporter status."
            )

            return redirect(
                "supporters:detail",
                pk=supporter.pk
            )

        supporter.status = status

        supporter.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            f"{supporter.full_name}'s status "
            f"was updated successfully."
        )

        return redirect(
            "supporters:detail",
            pk=supporter.pk
        )

# SUPPORTER EDIT

class SupporterEditView(
    SupportersManagerRequiredMixin,
    UpdateView
    ):
    model = Supporter
    form_class = SupporterEditForm
    template_name = "supporters/edit.html"
    context_object_name = "supporter"


    def get_success_url(self):
        return reverse(
            "supporters:detail",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            f"{self.object.full_name}'s information was updated successfully."
        )

        return super().form_valid(form)

