from django import forms

from works.models import Folder
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings

        fields = [
            "site_name",
            "banner",
            "logo",
            "intro_title",
            "intro_text",
            "telegram",
            "instagram",
            "rubika",
            "website",
        ]

        labels = {
            "site_name": "نام سایت",
            "banner": "بنر اصلی",
            "logo": "لوگو",
            "intro_title": "عنوان معرفی",
            "intro_text": "متن معرفی",
            "telegram": "تلگرام",
            "instagram": "اینستاگرام",
            "rubika": "روبیکا",
            "website": "وب‌سایت",
        }

        widgets = {
            "site_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "ABS ART",
                }
            ),
            "banner": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "intro_title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "عنوان معرفی",
                }
            ),
            "intro_text": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 7,
                    "placeholder": "متن معرفی ABS ART",
                }
            ),
            "telegram": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "لینک یا شناسه تلگرام",
                }
            ),
            "instagram": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "لینک یا شناسه اینستاگرام",
                }
            ),
            "rubika": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "لینک یا شناسه روبیکا",
                }
            ),
            "website": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "آدرس وب‌سایت",
                }
            ),
        }


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder

        fields = [
            "name",
            "custom_cover",
        ]

        labels = {
            "name": "نام پوشه",
            "custom_cover": "کاور اختصاصی",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "نام پوشه",
                }
            ),
            "custom_cover": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                }
            ),
        }


class SiteSecurityForm(forms.Form):

    password_1 = forms.CharField(
        label="رمز اصلی جدید",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "placeholder": "در صورت تغییر وارد کنید",
            }
        ),
    )

    password_1_confirm = forms.CharField(
        label="تکرار رمز اصلی",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "placeholder": "تکرار رمز اصلی",
            }
        ),
    )

    password_2 = forms.CharField(
        label="رمز جایگزین جدید",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "placeholder": "در صورت تغییر وارد کنید",
            }
        ),
    )

    password_2_confirm = forms.CharField(
        label="تکرار رمز جایگزین",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "placeholder": "تکرار رمز جایگزین",
            }
        ),
    )

    def clean(self):
        cleaned = super().clean()

        p1 = cleaned.get("password_1", "")
        p1c = cleaned.get("password_1_confirm", "")
        p2 = cleaned.get("password_2", "")
        p2c = cleaned.get("password_2_confirm", "")

        if p1 and p1 != p1c:
            self.add_error(
                "password_1_confirm",
                "تکرار رمز اصلی مطابقت ندارد."
            )

        if p2 and p2 != p2c:
            self.add_error(
                "password_2_confirm",
                "تکرار رمز جایگزین مطابقت ندارد."
            )

        return cleaned
