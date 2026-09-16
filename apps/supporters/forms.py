from django import forms

from .models import Supporter


class SupporterRegistrationForm(forms.ModelForm):

    class Meta:

        model = Supporter

        fields = [
            "full_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "lga",
            "ward",
            "community",
            "address",
            "occupation",
            "volunteer",
            "skills",
            "receive_updates",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "autocomplete": "name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 08012345678",
                    "autocomplete": "tel",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),

            "gender": forms.Select(),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "lga": forms.TextInput(
                attrs={
                    "placeholder": "Enter your LGA",
                }
            ),

            "ward": forms.TextInput(
                attrs={
                    "placeholder": "Enter your ward",
                }
            ),

            "community": forms.TextInput(
                attrs={
                    "placeholder": "Enter your community",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "placeholder": "Optional address",
                    "rows": 3,
                }
            ),

            "occupation": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Engineer, Trader, Student",
                }
            ),

            "skills": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Tell us about any skills you would "
                        "like to contribute."
                    ),
                    "rows": 4,
                }
            ),

            "volunteer": forms.CheckboxInput(),

            "receive_updates": forms.CheckboxInput(),
        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        phone = phone.strip()

        if not phone:
            raise forms.ValidationError(
                "Please provide a valid phone number."
            )

        return phone

    def clean_full_name(self):

        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 3:

            raise forms.ValidationError(
                "Please enter your full name."
            )

        return full_name

class SupporterEditForm(forms.ModelForm):


    class Meta:

        model = Supporter

        fields = [
            "full_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "lga",
            "ward",
            "community",
            "address",
            "occupation",
            "volunteer",
            "skills",
            "receive_updates",
            "status",
            "notes",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter full name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 08012345678",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                }
            ),

            "gender": forms.Select(),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "lga": forms.TextInput(
                attrs={
                    "placeholder": "Enter LGA",
                }
            ),

            "ward": forms.TextInput(
                attrs={
                    "placeholder": "Enter ward",
                }
            ),

            "community": forms.TextInput(
                attrs={
                    "placeholder": "Enter community",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "placeholder": "Enter address",
                    "rows": 3,
                }
            ),

            "occupation": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Engineer, Trader, Student",
                }
            ),

            "skills": forms.Textarea(
                attrs={
                    "placeholder": "Skills or areas of contribution",
                    "rows": 4,
                }
            ),

            "volunteer": forms.CheckboxInput(),

            "receive_updates": forms.CheckboxInput(),

            "status": forms.Select(),

            "notes": forms.Textarea(
                attrs={
                    "placeholder": "Internal administrative notes",
                    "rows": 5,
                }
            ),
        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"].strip()

        if not phone:
            raise forms.ValidationError(
                "Please provide a valid phone number."
            )

        return phone

    def clean_full_name(self):

        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 3:
            raise forms.ValidationError(
                "Please enter the full name."
            )

        return full_name

