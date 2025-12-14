"""URL configuration for AOC 2025 showcase."""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("aoc2025.web.showcase.urls")),
    # Redirect root to index view
    re_path(r"^showcase/?$", RedirectView.as_view(url="/", permanent=False)),
]
