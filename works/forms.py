from django import forms
from django.utils import timezone

from .models import Work


class WorkForm(forms.ModelForm):

    published_at = forms.DateTimeField(
        label="تاریخ و ساعت انتشار",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-input",
            },
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=[
            "%Y-%m-%dT%H:%M",
        ],
        required=True,
    )

    class Meta:
        model = Work

        fields = [
            "title",
            "description",
            "for_whom",
            "image",
            "folder",
            "status",
            "published_at",
            "is_showcase",
        ]

        labels = {
            "title": "عنوان طرح",
            "description": "توضیحات",
            "for_whom": "برای چه کسی",
            "image": "تصویر طرح",
            "folder": "پوشه",
            "status": "وضعیت",
            "is_showcase": "ویترین منتخب",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "عنوان طرح",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": "توضیحات طرح",
                }
            ),
            "for_whom": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "برای چه کسی",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "folder": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "is_showcase": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.initial["published_at"] = timezone.localtime().strftime(
                "%Y-%m-%dT%H:%M"
            )

