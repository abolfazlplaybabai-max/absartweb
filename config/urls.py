from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import (
    home,
    im_abs,
    im_abs_login,
    im_abs_logout,
    robots_txt,
    sitemap_xml,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "robots.txt",
        robots_txt,
        name="robots_txt",
    ),

    path(
        "sitemap.xml",
        sitemap_xml,
        name="sitemap_xml",
    ),

    path(
        "",
        home,
        name="home",
    ),

    path(
        "panel/",
        include("core.urls"),
    ),

    path(
        "works/",
        include("works.urls"),
    ),

    path(
        "im-abs/login/",
        im_abs_login,
        name="im_abs_login",
    ),

    path(
        "im-abs/",
        im_abs,
        name="im_abs",
    ),

    path(
        "im-abs/logout/",
        im_abs_logout,
        name="im_abs_logout",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )


# ABS ART custom error pages
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
