"""ASGI config for AOC 2025 showcase."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aoc2025.web.settings")

application = get_asgi_application()
