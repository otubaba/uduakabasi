from django import forms

from .models import ContactMessage, VolunteerApplication


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+234 800 000 0000",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "What would you like to discuss?",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here...",
                    "rows": 6,
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),
        }


class VolunteerApplicationForm(forms.ModelForm):

    class Meta:
        model = VolunteerApplication

        fields = [
            "name",
            "email",
            "phone",
            "location",
            "interest",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "autocomplete": "name",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+234 800 000 0000",
                    "autocomplete": "tel",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Uyo, Etinan, Nsit Ibom",
                    "autocomplete": "address-level2",
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "interest": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Tell us how you would like to contribute "
                        "to the movement..."
                    ),
                    "rows": 5,
                    "class": (
                        "w-full rounded-xl border border-slate-200 "
                        "bg-white px-4 py-3 text-sm text-slate-800 "
                        "outline-none transition "
                        "focus:border-campaign-blue "
                        "focus:ring-2 focus:ring-campaign-blue/10"
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Full Name"
        self.fields["email"].label = "Email Address"
        self.fields["phone"].label = "Phone Number"
        self.fields["location"].label = "Location"
        self.fields["interest"].label = "How would you like to help?"
        self.fields["message"].label = "Message"

        self.fields["email"].required = False
        self.fields["phone"].required = True
        self.fields["location"].required = True
        self.fields["message"].required = False