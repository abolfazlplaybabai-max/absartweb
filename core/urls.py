from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.panel_login, name="panel_login"),
    path("logout/", views.panel_logout, name="panel_logout"),

    path("", views.dashboard, name="dashboard"),

    path("works/", views.panel_work_list, name="panel_work_list"),
    path("works/new/", views.panel_work_create, name="panel_work_create"),
    path("works/<int:pk>/edit/", views.panel_work_edit, name="panel_work_edit"),
    path("works/<int:pk>/trash/", views.panel_work_trash, name="panel_work_trash"),
    path("works/<int:pk>/restore/", views.panel_work_restore, name="panel_work_restore"),
    path("works/<int:pk>/delete-permanently/", views.panel_work_delete_permanently, name="panel_work_delete_permanently"),

    path("drafts/", views.panel_drafts, name="panel_drafts"),
    path("trash/", views.panel_trash, name="panel_trash"),
    path("archive/", views.panel_archive, name="panel_archive"),

    path("folders/", views.panel_folder_list, name="panel_folder_list"),
    path("folders/new/", views.panel_folder_create, name="panel_folder_create"),
    path("folders/<int:pk>/edit/", views.panel_folder_edit, name="panel_folder_edit"),
    path("folders/<int:pk>/delete/", views.panel_folder_delete, name="panel_folder_delete"),

    path("showcase/", views.panel_showcase, name="panel_showcase"),
    path("showcase/<int:pk>/toggle/", views.panel_showcase_toggle, name="panel_showcase_toggle"),

    path("settings/", views.panel_site_settings, name="panel_site_settings"),

    path("preview/", views.panel_preview_list, name="panel_preview_list"),
    path("preview/<int:pk>/", views.panel_work_preview, name="panel_work_preview"),
    path("stats/", views.panel_stats, name="panel_stats"),
    path("security/", views.panel_security, name="panel_security"),
    path("maintenance/", views.panel_maintenance, name="panel_maintenance"),

]
