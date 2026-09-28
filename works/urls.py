from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.work_list,
        name="work_list",
    ),

    path(
        "folders/",
        views.folder_list,
        name="folder_list",
    ),

    path(
        "folders/<int:pk>/",
        views.folder_detail,
        name="folder_detail",
    ),

    path(
        "showcase/",
        views.showcase,
        name="showcase",
    ),

    path(
        "search/",
        views.search,
        name="search",
    ),

    path(
        "<int:pk>/",
        views.work_detail,
        name="work_detail",
    ),
    path("<int:pk>/like/", views.work_like_toggle, name="work_like_toggle"),
]

