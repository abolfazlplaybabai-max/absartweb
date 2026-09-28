from django.conf import settings
from django.urls import reverse
from works.models import Work, Folder


def site_url(request):
    return request.build_absolute_uri("/").rstrip("/")


def public_seo(request, title=None, description=None, image=None):
    base = site_url(request)

    data = {
        "seo_title": title or "ABS ART",
        "seo_description": (
            description
            or "ABS ART؛ مجموعه‌ای از طراحی‌ها و آثار گرافیکی."
        ),
        "seo_url": request.build_absolute_uri(),
        "seo_image": None,
        "seo_site_url": base,
    }

    if image:
        try:
            data["seo_image"] = request.build_absolute_uri(image.url)
        except Exception:
            data["seo_image"] = None

    return data


def public_sitemap_items(request):
    items = []

    items.append({
        "location": request.build_absolute_uri(reverse("home")),
        "changefreq": "weekly",
        "priority": "1.0",
    })

    items.append({
        "location": request.build_absolute_uri(reverse("work_list")),
        "changefreq": "daily",
        "priority": "0.9",
    })

    items.append({
        "location": request.build_absolute_uri(reverse("folder_list")),
        "changefreq": "weekly",
        "priority": "0.8",
    })

    items.append({
        "location": request.build_absolute_uri(reverse("showcase")),
        "changefreq": "weekly",
        "priority": "0.8",
    })

    for work in Work.objects.filter(
        status="active"
    ).select_related("folder").order_by("-published_at"):

        items.append({
            "location": request.build_absolute_uri(
                reverse("work_detail", args=[work.pk])
            ),
            "lastmod": work.updated_at,
            "changefreq": "monthly",
            "priority": "0.7",
        })

    for folder in Folder.objects.all().order_by("-updated_at"):

        items.append({
            "location": request.build_absolute_uri(
                reverse("folder_detail", args=[folder.pk])
            ),
            "lastmod": folder.updated_at,
            "changefreq": "weekly",
            "priority": "0.7",
        })

    return items
