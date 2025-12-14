.PHONY: help install login status new run test submit web clean

help:
	@echo "Kenneth's AOC 2025 Toolkit - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make login      - Login with session cookie"
	@echo "  make status     - Show current status"
	@echo "  make new DAY=N  - Create new day N"
	@echo "  make run DAY=N  - Run solution for day N"
	@echo "  make test DAY=N - Run solution with test input"
	@echo "  make submit DAY=N PART=P - Submit answer for day N part P"
	@echo "  make web        - Start Django web server"
	@echo "  make clean      - Clean build artifacts"
	@echo ""

install:
	uv sync

login:
	uv run aoc login

status:
	uv run aoc status

new:
	@if [ -z "$(DAY)" ]; then \
		echo "Error: DAY not set. Use: make new DAY=1"; \
		exit 1; \
	fi
	uv run aoc new $(DAY)

run:
	@if [ -z "$(DAY)" ]; then \
		echo "Error: DAY not set. Use: make run DAY=1"; \
		exit 1; \
	fi
	uv run aoc run $(DAY)

test:
	@if [ -z "$(DAY)" ]; then \
		echo "Error: DAY not set. Use: make test DAY=1"; \
		exit 1; \
	fi
	uv run aoc run $(DAY) --test

submit:
	@if [ -z "$(DAY)" ] || [ -z "$(PART)" ]; then \
		echo "Error: DAY or PART not set. Use: make submit DAY=1 PART=1"; \
		exit 1; \
	fi
	uv run aoc submit $(DAY) $(PART)

web:
	@echo "Starting Django web server..."
	@uv run python src/aoc2025/web/manage.py migrate --no-input 2>/dev/null || true
	uv run python src/aoc2025/web/manage.py runserver

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
