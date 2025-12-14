"""App configuration for showcase."""

from django.apps import AppConfig


class ShowcaseConfig(AppConfig):
    """Showcase app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "aoc2025.web.showcase"
