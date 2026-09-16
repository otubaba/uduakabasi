from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactMessageForm, VolunteerApplicationForm

from django.shortcuts import render

from apps.media.models import (
    MediaAlbum,
    MediaVideo,
)
from apps.events.models import Event
from apps.news.models import NewsArticle

from .models import (
    Agenda,
    CampaignProfile,
)


def home(request):

    profile = (
        CampaignProfile.objects
        .filter(is_active=True)
        .first()
    )


    agendas = (
        Agenda.objects
        .filter(is_active=True)
        .order_by("number")
    )


    latest_news = (
        NewsArticle.objects
        .filter(published=True)
        .select_related("category")
        .order_by(
            "-published_at",
            "-created_at",
        )[:3]
    )

    upcoming_events = (
        Event.objects
        .filter(
            published=True,
            status=Event.Status.UPCOMING,
        )
        .order_by(
            "event_date",
            "start_time",
        )[:3]
    )


    featured_albums = (
        MediaAlbum.objects
        .filter(
            published=True,
            featured=True,
        )
        .prefetch_related("images")
        .order_by(
            "display_order",
            "-event_date",
            "-created_at",
        )[:3]
    )


    latest_albums = (
        MediaAlbum.objects
        .filter(published=True)
        .prefetch_related("images")
        .order_by(
            "-event_date",
            "-created_at",
        )[:6]
    )


    featured_videos = (
        MediaVideo.objects
        .filter(
            published=True,
            featured=True,
        )
        .order_by(
            "display_order",
            "-published_at",
            "-created_at",
        )[:3]
    )


    latest_videos = (
        MediaVideo.objects
        .filter(published=True)
        .order_by(
            "-published_at",
            "-created_at",
        )[:3]
    )


    return render(
        request,
        "core/home.html",
        {
            "profile": profile,
            "agendas": agendas,
            "latest_news": latest_news,

            "featured_albums": featured_albums,
            "latest_albums": latest_albums,

            "featured_videos": featured_videos,
            "latest_videos": latest_videos,
            "upcoming_events": upcoming_events,
        }
    )


def about(request):
    profile = CampaignProfile.objects.filter(
        is_active=True
    ).first()

    return render(
        request,
        "core/about.html",
        {
            "profile": profile,
        }
    )


def agenda(request):
    profile = CampaignProfile.objects.filter(
        is_active=True
    ).first()

    agendas = Agenda.objects.filter(
        is_active=True
    ).order_by("number")

    return render(
        request,
        "core/agenda.html",
        {
            "profile": profile,
            "agendas": agendas,
        }
    )


def contact(request):

    profile = CampaignProfile.objects.filter(
        is_active=True
    ).first()


    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Thank you for contacting us. Your message has been received successfully."
            )

            return redirect("core:contact")

    else:

        form = ContactMessageForm()


    return render(
        request,
        "core/contact.html",
        {
            "profile": profile,
            "form": form,
        }
    )

def join_us(request):

    profile = CampaignProfile.objects.filter(
        is_active=True
    ).first()

    if request.method == "POST":

        form = VolunteerApplicationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                (
                    "Thank you for joining Uduak-Abasi 2027! "
                    "Your application has been received successfully."
                ),
            )

            return redirect("core:join_us")

    else:

        form = VolunteerApplicationForm()

    return render(
        request,
        "core/join.html",
        {
            "profile": profile,
            "form": form,
        },
    )

