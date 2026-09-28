from hashlib import sha256
from django.db import transaction
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render

from .models import Folder, Work, WorkLike


def work_list(request):

    works = (
        Work.objects
        .filter(status="active")
        .select_related("folder")
        .order_by("-published_at")
    )

    return render(
        request,
        "works/work_list.html",
        {
            "works": works,
        },
    )


def work_detail(request, pk):

    work = get_object_or_404(
        Work.objects.select_related("folder"),
        pk=pk,
        status="active",
    )

    if work.folder:

        other_works = (
            Work.objects
            .filter(
                status="active",
                folder=work.folder,
            )
            .exclude(pk=work.pk)
            .order_by("-published_at")[:3]
        )

    else:

        other_works = (
            Work.objects
            .filter(status="active")
            .exclude(pk=work.pk)
            .order_by("-published_at")[:3]
        )

    ip_address = request.META.get("REMOTE_ADDR", "")
    liked_by_ip = False

    if ip_address:
        ip_hash = sha256(
            f"{settings.SECRET_KEY}:{ip_address}".encode("utf-8")
        ).hexdigest()

        liked_by_ip = WorkLike.objects.filter(
            work=work,
            ip_hash=ip_hash,
        ).exists()

    return render(
        request,
        "works/work_detail.html",
        {
            "work": work,
            "other_works": other_works,
            "like_count": work.likes.count(),
            "liked_by_ip": liked_by_ip,
        },
    )



@require_POST
def work_like_toggle(request, pk):
    work = get_object_or_404(
        Work,
        pk=pk,
        status="active",
    )

    ip_address = request.META.get("REMOTE_ADDR", "")

    if not ip_address:
        return JsonResponse(
            {
                "ok": False,
                "message": "شناسه اتصال قابل تشخیص نیست.",
            },
            status=400,
        )

    ip_hash = sha256(
        f"{settings.SECRET_KEY}:{ip_address}".encode("utf-8")
    ).hexdigest()

    with transaction.atomic():
        like = (
            WorkLike.objects
            .select_for_update()
            .filter(
                work=work,
                ip_hash=ip_hash,
            )
            .first()
        )

        if like:
            like.delete()
            liked = False
        else:
            WorkLike.objects.create(
                work=work,
                ip_hash=ip_hash,
            )
            liked = True

    like_count = WorkLike.objects.filter(work=work).count()

    return JsonResponse(
        {
            "ok": True,
            "liked": liked,
            "count": like_count,
        }
    )

def folder_list(request):

    folders = (
        Folder.objects
        .all()
        .order_by("-updated_at")
    )

    folder_data = []

    for folder in folders:

        latest_work = (
            Work.objects
            .filter(
                folder=folder,
                status="active",
            )
            .order_by("-published_at")
            .first()
        )

        folder_data.append(
            {
                "folder": folder,
                "latest_work": latest_work,
            }
        )

    return render(
        request,
        "works/folder_list.html",
        {
            "folder_data": folder_data,
        },
    )


def folder_detail(request, pk):

    folder = get_object_or_404(
        Folder,
        pk=pk,
    )

    works = (
        Work.objects
        .filter(
            folder=folder,
            status="active",
        )
        .order_by("-published_at")
    )

    return render(
        request,
        "works/folder_detail.html",
        {
            "folder": folder,
            "works": works,
        },
    )


def showcase(request):

    works = (
        Work.objects
        .filter(
            status="active",
            is_showcase=True,
        )
        .select_related("folder")
        .order_by("-published_at")
    )

    return render(
        request,
        "works/showcase.html",
        {
            "works": works,
        },
    )


def search(request):

    query = request.GET.get("q", "").strip()

    works = Work.objects.none()
    folders = Folder.objects.none()

    if query:

        works = (
            Work.objects
            .filter(status="active")
            .filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(for_whom__icontains=query)
                | Q(folder__name__icontains=query)
            )
            .select_related("folder")
            .order_by("-published_at")
        )

        folders = (
            Folder.objects
            .filter(
                Q(name__icontains=query)
            )
            .order_by("-updated_at")
        )

    return render(
        request,
        "works/search.html",
        {
            "query": query,
            "works": works,
            "folders": folders,
        },
    )

