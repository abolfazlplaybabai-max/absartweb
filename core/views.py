from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from works.forms import WorkForm
from works.models import Folder, Work, WorkLike

from .seo import public_sitemap_items
from .forms import SiteSettingsForm, FolderForm, SiteSecurityForm
from .models import SiteSettings, SiteSecurity


# =========================================================
# PUBLIC
# =========================================================

def home(request):
    latest_works = (
        Work.objects
        .filter(status="active")
        .select_related("folder")
        .order_by("-published_at")[:6]
    )

    latest_work = latest_works[0] if latest_works else None

    site_settings = (
        SiteSettings.objects
        .order_by("-updated_at")
        .first()
    )

    return render(
        request,
        "core/home.html",
        {
            "latest_work": latest_work,
            "latest_works": latest_works,
            "site_settings": site_settings,
        },
    )


# =========================================================
# PANEL AUTH
# =========================================================

def panel_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد پنل شدید.")
            return redirect("dashboard")

        messages.error(request, "نام کاربری یا رمز عبور نادرست است.")

    return render(request, "core/panel_login.html")


@login_required
def panel_logout(request):
    logout(request)
    messages.success(request, "با موفقیت از پنل خارج شدید.")
    return redirect("panel_login")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):
    total_works = Work.objects.exclude(status="trash").count()
    active_works = Work.objects.filter(status="active").count()
    draft_works = Work.objects.filter(status="draft").count()
    inactive_works = Work.objects.filter(status="inactive").count()
    trash_works = Work.objects.filter(status="trash").count()
    showcase_works = Work.objects.filter(
        status="active",
        is_showcase=True,
    ).count()
    total_folders = Folder.objects.count()

    return render(
        request,
        "core/dashboard.html",
        {
            "total_works": total_works,
            "active_works": active_works,
            "draft_works": draft_works,
            "inactive_works": inactive_works,
            "trash_works": trash_works,
            "showcase_works": showcase_works,
            "total_folders": total_folders,

            # aliases for template compatibility
            "works_count": total_works,
            "active_count": active_works,
            "draft_count": draft_works,
            "inactive_count": inactive_works,
            "trash_count": trash_works,
            "showcase_count": showcase_works,
            "folders_count": total_folders,
        },
    )


# =========================================================
# WORK MANAGEMENT
# =========================================================

@login_required
def panel_work_list(request):
    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    works = Work.objects.select_related("folder").all()

    if query:
        works = works.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(for_whom__icontains=query)
            | Q(folder__name__icontains=query)
        )

    if status_filter in {"active", "draft", "inactive", "trash"}:
        works = works.filter(status=status_filter)
    else:
        works = works.exclude(status="trash")

    sort_map = {
        "newest": "-published_at",
        "oldest": "published_at",
        "updated": "-updated_at",
        "title": "title",
    }

    works = works.order_by(sort_map.get(sort, "-published_at"))

    return render(
        request,
        "core/panel_work_list.html",
        {
            "works": works,
            "query": query,
            "status_filter": status_filter,
            "sort": sort,
        },
    )


@login_required
def panel_work_create(request):
    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES)

        if form.is_valid():
            work = form.save()

            if work.status != "active":
                work.is_showcase = False
                work.save(update_fields=["is_showcase"])

            messages.success(
                request,
                f"طرح «{work.title}» با موفقیت ایجاد شد.",
            )
            return redirect("panel_work_list")
    else:
        form = WorkForm()

    return render(
        request,
        "core/panel_work_form.html",
        {
            "form": form,
            "page_title": "افزودن طرح",
            "submit_text": "ذخیره طرح",
        },
    )


@login_required
def panel_work_edit(request, pk):
    work = get_object_or_404(Work, pk=pk)

    if request.method == "POST":
        form = WorkForm(
            request.POST,
            request.FILES,
            instance=work,
        )

        if form.is_valid():
            work = form.save()

            if work.status != "active":
                work.is_showcase = False
                work.save(update_fields=["is_showcase"])

            messages.success(
                request,
                f"طرح «{work.title}» با موفقیت ویرایش شد.",
            )
            return redirect("panel_work_list")
    else:
        form = WorkForm(instance=work)

    return render(
        request,
        "core/panel_work_form.html",
        {
            "form": form,
            "work": work,
            "page_title": "ویرایش طرح",
            "submit_text": "ذخیره تغییرات",
        },
    )


@login_required
@require_POST
def panel_work_trash(request, pk):
    work = get_object_or_404(Work, pk=pk)

    work.status = "trash"
    work.deleted_at = timezone.now()
    work.is_showcase = False
    work.save(
        update_fields=[
            "status",
            "deleted_at",
            "is_showcase",
            "updated_at",
        ]
    )

    messages.success(
        request,
        f"طرح «{work.title}» به سطل بازیابی منتقل شد.",
    )

    return redirect(request.META.get("HTTP_REFERER") or "panel_work_list")


@login_required
@require_POST
def panel_work_restore(request, pk):
    work = get_object_or_404(
        Work,
        pk=pk,
        status="trash",
    )

    work.status = "draft"
    work.deleted_at = None
    work.save(
        update_fields=[
            "status",
            "deleted_at",
            "updated_at",
        ]
    )

    messages.success(
        request,
        f"طرح «{work.title}» بازیابی شد و به پیش‌نویس برگشت.",
    )

    return redirect(request.META.get("HTTP_REFERER") or "panel_trash")


@login_required
@require_POST
def panel_work_delete_permanently(request, pk):
    work = get_object_or_404(Work, pk=pk)

    title = work.title

    if work.image:
        try:
            work.image.delete(save=False)
        except Exception:
            pass

    work.delete()

    messages.success(
        request,
        f"طرح «{title}» برای همیشه حذف شد.",
    )

    return redirect(request.META.get("HTTP_REFERER") or "panel_trash")


@login_required
def panel_drafts(request):
    works = (
        Work.objects
        .filter(status="draft")
        .select_related("folder")
        .order_by("-updated_at")
    )

    return render(
        request,
        "core/panel_drafts.html",
        {
            "works": works,
        },
    )


@login_required
def panel_trash(request):
    works = (
        Work.objects
        .filter(status="trash")
        .select_related("folder")
        .order_by("-deleted_at", "-updated_at")
    )

    return render(
        request,
        "core/panel_trash.html",
        {
            "works": works,
        },
    )


@login_required
def panel_archive(request):
    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    works = Work.objects.select_related("folder").all()

    if query:
        works = works.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(for_whom__icontains=query)
            | Q(folder__name__icontains=query)
        )

    if status_filter in {"active", "draft", "inactive", "trash"}:
        works = works.filter(status=status_filter)

    sort_map = {
        "newest": "-published_at",
        "oldest": "published_at",
        "updated": "-updated_at",
        "title": "title",
    }

    works = works.order_by(sort_map.get(sort, "-published_at"))

    return render(
        request,
        "core/panel_archive.html",
        {
            "works": works,
            "query": query,
            "status_filter": status_filter,
            "sort": sort,
        },
    )


# =========================================================
# FOLDER MANAGEMENT
# =========================================================

@login_required
def panel_folder_list(request):
    folders = Folder.objects.annotate(
        active_work_count=Count(
            "works",
            filter=Q(works__status="active"),
        )
    ).order_by("-updated_at")

    return render(
        request,
        "core/panel_folder_list.html",
        {
            "folders": folders,
        },
    )


@login_required
def panel_folder_create(request):
    if request.method == "POST":
        form = FolderForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            folder = form.save()

            messages.success(
                request,
                f"پوشه «{folder.name}» با موفقیت ایجاد شد.",
            )

            return redirect("panel_folder_list")
    else:
        form = FolderForm()

    return render(
        request,
        "core/panel_folder_form.html",
        {
            "form": form,
            "page_title": "افزودن پوشه",
            "submit_text": "ذخیره پوشه",
        },
    )


@login_required
def panel_folder_edit(request, pk):
    folder = get_object_or_404(Folder, pk=pk)

    if request.method == "POST":
        form = FolderForm(
            request.POST,
            request.FILES,
            instance=folder,
        )

        if form.is_valid():
            folder = form.save()

            messages.success(
                request,
                f"پوشه «{folder.name}» با موفقیت ویرایش شد.",
            )

            return redirect("panel_folder_list")
    else:
        form = FolderForm(instance=folder)

    return render(
        request,
        "core/panel_folder_form.html",
        {
            "form": form,
            "folder": folder,
            "page_title": "ویرایش پوشه",
            "submit_text": "ذخیره تغییرات",
        },
    )


@login_required
@require_POST
def panel_folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk)

    name = folder.name

    if folder.custom_cover:
        try:
            folder.custom_cover.delete(save=False)
        except Exception:
            pass

    folder.delete()

    messages.success(
        request,
        f"پوشه «{name}» حذف شد.",
    )

    return redirect("panel_folder_list")


# =========================================================
# SHOWCASE
# =========================================================

@login_required
def panel_showcase(request):
    works = (
        Work.objects
        .filter(status="active")
        .select_related("folder")
        .order_by("-is_showcase", "-published_at")
    )

    return render(
        request,
        "core/panel_showcase.html",
        {
            "works": works,
        },
    )


@login_required
@require_POST
def panel_showcase_toggle(request, pk):
    work = get_object_or_404(
        Work,
        pk=pk,
    )

    if work.status != "active":
        work.is_showcase = False
        work.save(update_fields=["is_showcase", "updated_at"])

        messages.warning(
            request,
            "فقط طرح‌های فعال می‌توانند در ویترین منتخب باشند.",
        )

        return redirect("panel_showcase")

    work.is_showcase = not work.is_showcase
    work.save(
        update_fields=[
            "is_showcase",
            "updated_at",
        ]
    )

    if work.is_showcase:
        messages.success(
            request,
            f"طرح «{work.title}» به ویترین منتخب اضافه شد.",
        )
    else:
        messages.success(
            request,
            f"طرح «{work.title}» از ویترین منتخب حذف شد.",
        )

    return redirect("panel_showcase")


# =========================================================
# SITE SETTINGS
# =========================================================

@login_required
def panel_site_settings(request):
    site_settings = (
        SiteSettings.objects
        .order_by("-updated_at")
        .first()
    )

    if site_settings is None:
        site_settings = SiteSettings.objects.create(
            site_name="ABS ART",
        )

    if request.method == "POST":
        form = SiteSettingsForm(
            request.POST,
            request.FILES,
            instance=site_settings,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "تنظیمات سایت با موفقیت ذخیره شد.",
            )

            return redirect("panel_site_settings")
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(
        request,
        "core/panel_site_settings.html",
        {
            "form": form,
            "site_settings": site_settings,
        },
    )


# =========================================================
# PREVIEW
# =========================================================

@login_required
def panel_preview_list(request):
    works = (
        Work.objects
        .exclude(status="trash")
        .select_related("folder")
        .order_by("-published_at")
    )

    return render(
        request,
        "core/panel_preview_list.html",
        {
            "works": works,
        },
    )


@login_required
def panel_work_preview(request, pk):
    work = get_object_or_404(
        Work.objects.select_related("folder"),
        pk=pk,
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

    return render(
        request,
        "works/work_detail.html",
        {
            "work": work,
            "other_works": other_works,
            "like_count": WorkLike.objects.filter(work=work).count(),
            "liked_by_ip": False,
            "preview_mode": True,
        },
    )


# =========================================================
# STATISTICS
# =========================================================

@login_required
def panel_stats(request):
    total_works = Work.objects.count()
    active_works = Work.objects.filter(status="active").count()
    draft_works = Work.objects.filter(status="draft").count()
    inactive_works = Work.objects.filter(status="inactive").count()
    trash_works = Work.objects.filter(status="trash").count()
    showcase_works = Work.objects.filter(
        status="active",
        is_showcase=True,
    ).count()
    total_folders = Folder.objects.count()

    folder_stats = (
        Folder.objects
        .annotate(
            active_count=Count(
                "works",
                filter=Q(works__status="active"),
            )
        )
        .order_by("-active_count", "name")
    )

    return render(
        request,
        "core/panel_stats.html",
        {
            "total_works": total_works,
            "active_works": active_works,
            "draft_works": draft_works,
            "inactive_works": inactive_works,
            "trash_works": trash_works,
            "showcase_works": showcase_works,
            "total_folders": total_folders,
            "folder_stats": folder_stats,
        },
    )


# =========================================================
# SECURITY
# =========================================================

@login_required
def panel_security(request):
    security = (
        SiteSecurity.objects
        .order_by("-updated_at")
        .first()
    )

    if security is None:
        security = SiteSecurity.objects.create()

    if request.method == "POST":
        form = SiteSecurityForm(request.POST)

        if form.is_valid():
            password_1 = form.cleaned_data.get("password_1")
            password_2 = form.cleaned_data.get("password_2")

            changed = False

            if password_1:
                security.password_hash_1 = make_password(password_1)
                changed = True

            if password_2:
                security.password_hash_2 = make_password(password_2)
                changed = True

            if changed:
                security.save()

                messages.success(
                    request,
                    "تنظیمات امنیتی با موفقیت ذخیره شد.",
                )
            else:
                messages.info(
                    request,
                    "رمز جدیدی وارد نشده بود.",
                )

            return redirect("panel_security")
    else:
        form = SiteSecurityForm()

    return render(
        request,
        "core/panel_security.html",
        {
            "form": form,
            "security": security,
        },
    )


# =========================================================
# MAINTENANCE
# =========================================================

@login_required
def panel_maintenance(request):
    site_settings = (
        SiteSettings.objects
        .order_by("-updated_at")
        .first()
    )

    if site_settings is None:
        site_settings = SiteSettings.objects.create(
            site_name="ABS ART",
        )

    if request.method == "POST":
        site_settings.maintenance_mode = not site_settings.maintenance_mode
        site_settings.save(update_fields=["maintenance_mode", "updated_at"])

        if site_settings.maintenance_mode:
            messages.success(
                request,
                "حالت تعمیرات فعال شد.",
            )
        else:
            messages.success(
                request,
                "حالت تعمیرات غیرفعال شد.",
            )

        return redirect("panel_maintenance")

    return render(
        request,
        "core/panel_maintenance.html",
        {
            "site_settings": site_settings,
            "maintenance_mode": site_settings.maintenance_mode,
        },
    )


# =========================================================
# I'M ABS
# =========================================================

def im_abs_login(request):
    if request.session.get("im_abs_authenticated"):
        return redirect("im_abs")

    if request.method == "POST":
        password = request.POST.get("password", "")

        security = (
            SiteSecurity.objects
            .order_by("-updated_at")
            .first()
        )

        valid = False

        if security:
            if security.password_hash_1:
                from django.contrib.auth.hashers import check_password

                if check_password(
                    password,
                    security.password_hash_1,
                ):
                    valid = True

            if not valid and security.password_hash_2:
                from django.contrib.auth.hashers import check_password

                if check_password(
                    password,
                    security.password_hash_2,
                ):
                    valid = True

        if valid:
            request.session["im_abs_authenticated"] = True
            return redirect("im_abs")

        messages.error(
            request,
            "رمز عبور نادرست است.",
        )

    return render(
        request,
        "core/im_abs_login.html",
    )


def im_abs(request):
    if not request.session.get("im_abs_authenticated"):
        return redirect("im_abs_login")

    return render(
        request,
        "core/im_abs.html",
    )


def im_abs_logout(request):
    request.session.pop("im_abs_authenticated", None)
    return redirect("im_abs_login")


# =========================================================
# SEO
# =========================================================

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain; charset=utf-8",
    )


@require_GET
def sitemap_xml(request):
    items = public_sitemap_items(request)

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for item in items:
        xml.append("<url>")
        xml.append(f"<loc>{item['loc']}</loc>")

        if item.get("lastmod"):
            xml.append(
                f"<lastmod>{item['lastmod']}</lastmod>"
            )

        xml.append("</url>")

    xml.append("</urlset>")

    return HttpResponse(
        "\n".join(xml),
        content_type="application/xml; charset=utf-8",
    )


# =========================================================
# ERROR PAGES
# =========================================================

def error_404(request, exception):
    return render(
        request,
        "404.html",
        status=404,
    )


def error_500(request):
    return render(
        request,
        "500.html",
        status=500,
    )
