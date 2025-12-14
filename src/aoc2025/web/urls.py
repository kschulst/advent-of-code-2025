"""URL configuration for AOC 2025 showcase."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("aoc2025.web.showcase.urls")),
]
