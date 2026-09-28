from django.shortcuts import render

from .models import SiteSettings


class MaintenanceMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        allowed = (
            path.startswith("/panel/"),
            path.startswith("/admin/"),
            path.startswith("/im-abs/"),
            path.startswith("/media/"),
            path.startswith("/static/"),
        )

        if any(allowed):
            return self.get_response(request)

        settings_instance = (
            SiteSettings.objects
            .order_by("-updated_at")
            .first()
        )

        if (
            settings_instance
            and settings_instance.maintenance_mode
        ):
            return render(
                request,
                "core/maintenance.html",
                status=503,
            )

        return self.get_response(request)
