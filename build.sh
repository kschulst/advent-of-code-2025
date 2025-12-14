#!/usr/bin/env bash
# exit on error
set -o errexit

# Install uv
pip install uv

# Install dependencies
uv sync

# Collect static files
uv run python src/aoc2025/web/manage.py collectstatic --no-input

# Run migrations
uv run python src/aoc2025/web/manage.py migrate
