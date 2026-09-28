from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "site_name",
                    "logo",
                    "banner",
                )
            },
        ),
        (
            "معرفی ABS ART",
            {
                "fields": (
                    "intro_title",
                    "intro_text",
                )
            },
        ),
        (
            "شبکه‌های اجتماعی و لینک‌ها",
            {
                "fields": (
                    "telegram",
                    "instagram",
                    "rubika",
                    "website",
                )
            },
        ),
    )

    readonly_fields = (
        "updated_at",
    )

