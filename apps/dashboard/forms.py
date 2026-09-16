from django import forms

from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle

        fields = [
            "category",
            "content_type",
            "title",
            "excerpt",
            "content",
            "featured_image",
            "video",
            "video_url",
            "published",
            "published_at",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "content_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter news article title",
                }
            ),

            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write a short summary of the article...",
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 14,
                    "placeholder": "Write the full news article...",
                }
            ),

            "featured_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "video": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "video/*",
                }
            ),

            "video_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://youtube.com/...",
                }
            ),

            "published": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),

            "published_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
        }