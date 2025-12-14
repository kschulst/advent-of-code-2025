"""Views for showcase app."""

import importlib.util
import sys

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from aoc2025.api import AOCClient
from aoc2025.config import settings as aoc_settings
from aoc2025.scaffold import DayScaffold


def index(request: HttpRequest):
    """Show all completed days."""
    solutions_dir = aoc_settings.solutions_dir

    days = []
    if solutions_dir.exists():
        for day_dir in sorted(solutions_dir.iterdir()):
            if day_dir.is_dir() and day_dir.name.startswith("day_"):
                day_num = int(day_dir.name.split("_")[1])
                solution_path = day_dir / "solution.py"
                input_path = day_dir / "input.txt"

                days.append(
                    {
                        "number": day_num,
                        "has_solution": solution_path.exists(),
                        "has_input": input_path.exists(),
                    }
                )

    context = {"days": days, "year": 2025}
    return render(request, "showcase/index.html", context)


def day_detail(request: HttpRequest, day: int):
    """Show detail for a specific day."""
    scaffold = DayScaffold(day)
    solution_path = scaffold.get_solution_path()
    input_path = scaffold.get_input_path()
    readme_path = scaffold.day_dir / "README.md"

    context = {
        "day": day,
        "year": 2025,
        "has_solution": solution_path.exists(),
        "has_input": input_path.exists(),
        "aoc_url": f"https://adventofcode.com/2025/day/{day}",
    }

    # Load solution code
    if solution_path.exists():
        context["solution_code"] = solution_path.read_text()

        # Try to run the solution
        try:
            spec = importlib.util.spec_from_file_location(
                f"day_{day:02d}.solution", solution_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"day_{day:02d}.solution"] = module
                spec.loader.exec_module(module)

                if input_path.exists():
                    Solution = module.Solution
                    solution = Solution.from_file(input_path)

                    try:
                        context["part1_answer"] = str(solution.part_1())
                    except NotImplementedError:
                        context["part1_answer"] = "Not implemented"

                    try:
                        context["part2_answer"] = str(solution.part_2())
                    except NotImplementedError:
                        context["part2_answer"] = "Not implemented"
        except Exception as e:
            context["error"] = str(e)

    # Load input text
    if input_path.exists():
        input_text = input_path.read_text()
        context["input_text"] = input_text
        context["input_line_count"] = len(input_text.splitlines())

    # Load README
    if readme_path.exists():
        context["readme"] = readme_path.read_text()

    return render(request, "showcase/day_detail.html", context)


def download_input_api(request: HttpRequest, day: int):
    """API endpoint to download input for a day."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        client = AOCClient()
        scaffold = DayScaffold(day)
        input_path = scaffold.get_input_path()

        client.download_input(day, output_path=input_path)

        return JsonResponse(
            {"success": True, "message": f"Downloaded input for day {day}"}
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
