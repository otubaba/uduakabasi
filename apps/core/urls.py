from django.urls import path
from . import views


app_name = "core"


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("agenda/", views.agenda, name="agenda"),
    path("contact/", views.contact, name="contact"),
    path(
        "join-us/",
        views.join_us,
        name="join_us",
    ),
]