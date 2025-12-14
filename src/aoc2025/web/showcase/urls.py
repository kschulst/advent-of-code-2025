"""URLs for showcase app."""

from django.urls import path

from . import views

app_name = "showcase"

urlpatterns = [
    path("", views.index, name="index"),
    path("day/<int:day>/", views.day_detail, name="day_detail"),
    path(
        "api/download-input/<int:day>/", views.download_input_api, name="download_input"
    ),
]
