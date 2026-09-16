from django.views.generic import ListView, DetailView

from .models import Event
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# =========================================================
# EVENT LIST
# =========================================================

class EventListView(ListView):

    model = Event

    template_name = "events/list.html"

    context_object_name = "events"

    paginate_by = 9

    def get_queryset(self):

        return (
            Event.objects
            .filter(
                published=True
            )
            .order_by(
                "event_date",
                "start_time",
                "-created_at",
            )
        )


# =========================================================
# EVENT DETAIL
# =========================================================

class EventDetailView(DetailView):

    model = Event

    template_name = "events/detail.html"

    context_object_name = "event"

    slug_field = "slug"

    slug_url_kwarg = "slug"

    def get_queryset(self):

        return Event.objects.filter(
            published=True
        )

class EventsManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_active
            and (
                self.request.user.is_superuser
                or self.request.user.groups.filter(
                    name="Events Manager"
                ).exists()
            )
        )

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(
            self.request,
            "You do not have permission to manage events."
        )

        return redirect("dashboard:home")

        