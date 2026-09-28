from django.db import models
from django.utils import timezone


class Folder(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام پوشه")
    custom_cover = models.ImageField(
        upload_to="folders/covers/",
        blank=True,
        null=True,
        verbose_name="کاور اختصاصی"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "پوشه"
        verbose_name_plural = "پوشه‌ها"

    def __str__(self):
        return self.name


class Work(models.Model):
    STATUS_CHOICES = [
        ("active", "فعال"),
        ("draft", "پیش‌نویس"),
        ("inactive", "غیرفعال"),
        ("trash", "سطل بازیابی"),
    ]

    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    for_whom = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="برای چه کسی"
    )
    image = models.ImageField(
        upload_to="works/%Y/%m/",
        verbose_name="تصویر"
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="works",
        verbose_name="پوشه"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="وضعیت"
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ و ساعت انتشار"
    )
    is_showcase = models.BooleanField(
        default=False,
        verbose_name="ویترین منتخب"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان انتقال به سطل"
    )

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "طرح"
        verbose_name_plural = "طرح‌ها"

    def __str__(self):
        return self.title

    @property
    def is_new(self):
        if self.status != "active":
            return False

        age = timezone.now() - self.published_at
        return age.total_seconds() < 48 * 60 * 60


class WorkLike(models.Model):
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="لایک‌ها",
    )
    ip_hash = models.CharField(
        max_length=64,
        verbose_name="شناسه ناشناس IP",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "لایک طرح"
        verbose_name_plural = "لایک‌های طرح"
        constraints = [
            models.UniqueConstraint(
                fields=["work", "ip_hash"],
                name="unique_work_ip_like",
            )
        ]

    def __str__(self):
        return f"{self.work} - {self.ip_hash[:12]}"
