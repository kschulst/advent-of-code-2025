"""WSGI config for AOC 2025 showcase."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aoc2025.web.settings")

application = get_wsgi_application()
