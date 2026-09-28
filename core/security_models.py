from django.db import models


class SiteSecurity(models.Model):

    password_hash_1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="رمز اصلی"
    )

    password_hash_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="رمز جایگزین"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "امنیت سایت"
        verbose_name_plural = "امنیت سایت"

    def __str__(self):
        return "تنظیمات امنیتی ABS ART"

