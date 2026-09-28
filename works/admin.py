from django.contrib import admin
from .models import Folder, Work


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    search_fields = ("name",)
    ordering = ("-updated_at",)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "folder",
        "status",
        "published_at",
        "is_showcase",
    )
    list_filter = (
        "status",
        "is_showcase",
        "folder",
    )
    search_fields = (
        "title",
        "description",
        "for_whom",
    )
    ordering = ("-published_at",)
    list_editable = (
        "status",
        "is_showcase",
    )
