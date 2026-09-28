from django.db import models


class SiteSettings(models.Model):

    site_name = models.CharField(
        max_length=100,
        default="ABS ART",
        verbose_name="نام سایت"
    )

    banner = models.ImageField(
        upload_to="site/banner/",
        blank=True,
        null=True,
        verbose_name="بنر اصلی"
    )

    logo = models.ImageField(
        upload_to="site/logo/",
        blank=True,
        null=True,
        verbose_name="لوگو"
    )

    intro_title = models.CharField(
        max_length=250,
        default="ABS ART",
        verbose_name="عنوان معرفی"
    )

    intro_text = models.TextField(
        blank=True,
        verbose_name="متن معرفی"
    )

    telegram = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="تلگرام"
    )

    instagram = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="اینستاگرام"
    )

    rubika = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="روبیکا"
    )

    website = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="وب‌سایت"
    )

    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="حالت تعمیرات"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name


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

    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="حالت تعمیرات"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "امنیت سایت"
        verbose_name_plural = "امنیت سایت"

    def __str__(self):
        return "تنظیمات امنیتی ABS ART"

