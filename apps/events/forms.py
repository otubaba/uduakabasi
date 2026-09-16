from django import forms

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            "title",
            "short_description",
            "description",
            "featured_image",
            "event_date",
            "start_time",
            "end_time",
            "venue",
            "location",
            "address",
            "status",
            "registration_open",
            "registration_url",
            "featured",
            "published",
        ]

        widgets = {

            # =================================================
            # BASIC INFORMATION
            # =================================================

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event title",
                }
            ),

            "short_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Write a short summary of the event..."
                    ),
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": (
                        "Write the full event description..."
                    ),
                }
            ),

            # =================================================
            # IMAGE
            # =================================================

            "featured_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            # =================================================
            # DATE & TIME
            # =================================================

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            # =================================================
            # LOCATION
            # =================================================

            "venue": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Uyo Township Stadium",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "e.g. Uyo, Akwa Ibom State"
                    ),
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Enter the complete event address..."
                    ),
                }
            ),

            # =================================================
            # STATUS
            # =================================================

            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            # =================================================
            # REGISTRATION
            # =================================================

            "registration_open": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),

            "registration_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "https://example.com/register"
                    ),
                }
            ),

            # =================================================
            # WEBSITE DISPLAY
            # =================================================

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),

            "published": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }