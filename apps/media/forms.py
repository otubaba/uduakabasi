from django import forms

from .models import MediaAlbum, MediaImage, MediaVideo


# ============================================================
# MEDIA ALBUM FORM
# ============================================================

class MediaAlbumForm(forms.ModelForm):

    class Meta:
        model = MediaAlbum

        fields = [
            "title",
            "description",
            "cover_image",
            "event_date",
            "location",
            "featured",
            "published",
            "display_order",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter album title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe this gallery album...",
                }
            ),

            "cover_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Uyo, Akwa Ibom State",
                }
            ),

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

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }


# ============================================================
# MEDIA IMAGE FORM
# ============================================================

class MediaImageForm(forms.ModelForm):

    class Meta:
        model = MediaImage

        fields = [
            "image",
            "caption",
            "alt_text",
            "display_order",
        ]

        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional image caption",
                }
            ),

            "alt_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the image for accessibility",
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }


# ============================================================
# MEDIA VIDEO FORM
# ============================================================

class MediaVideoForm(forms.ModelForm):

    # Video URL is optional
    video_url = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.youtube.com/watch?v=...",
            }
        ),
    )

    class Meta:
        model = MediaVideo

        fields = [
            "title",
            "description",
            "thumbnail",
            "video_url",
            "video_type",
            "duration",
            "published_at",
            "featured",
            "published",
            "display_order",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter video title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe this video...",
                }
            ),

            "thumbnail": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "video_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "duration": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 12:35",
                }
            ),

            "published_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

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

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [
                single_file_clean(file, initial)
                for file in data
            ]

        return [single_file_clean(data, initial)]


class MediaBulkImageUploadForm(forms.Form):

    images = MultipleFileField(
        required=True,
        widget=MultipleFileInput(
            attrs={
                "accept": "image/*",
                "class": "form-control",
            }
        ),
        help_text="Select multiple images to upload to this album.",
    )

    def clean_images(self):

        files = self.cleaned_data["images"]

        if not files:
            raise forms.ValidationError(
                "Please select at least one image."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif",
        ]

        max_size = 5 * 1024 * 1024

        for image in files:

            if image.content_type not in allowed_types:

                raise forms.ValidationError(
                    f"{image.name} is not a supported image format."
                )

            if image.size > max_size:

                raise forms.ValidationError(
                    f"{image.name} is larger than 5MB."
                )

        return files
    
