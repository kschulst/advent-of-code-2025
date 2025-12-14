"""Scaffolding utilities for creating new day solutions."""

from pathlib import Path

from rich.console import Console

from .config import settings

console = Console()

SOLUTION_TEMPLATE = '''"""Solution for Advent of Code {year} - Day {day}."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day {day}."""

    day = {day}
    year = {year}

    def part_1(self) -> int | str:
        """Solve part 1."""
        # TODO: Implement solution for part 1
        return 0

    def part_2(self) -> int | str:
        """Solve part 2."""
        # TODO: Implement solution for part 2
        return 0


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {{solution.part_1()}}")
    print(f"Part 2: {{solution.part_2()}}")
'''

INIT_TEMPLATE = '''"""Day {day} solution package."""

from .solution import Solution

__all__ = ["Solution"]
'''

README_TEMPLATE = """# Day {day}: [Title TBD]

## Part 1

TODO: Add notes about part 1

## Part 2

TODO: Add notes about part 2

## Approach

TODO: Describe your solution approach
"""


class DayScaffold:
    """Create scaffolding for a new day's solution."""

    def __init__(self, day: int, year: int = 2025):
        """Initialize scaffold generator."""
        if not 1 <= day <= 25:
            raise ValueError(f"Day must be between 1 and 25, got {day}")

        self.day = day
        self.year = year
        self.day_dir = settings.solutions_dir / f"day_{day:02d}"

    def create(self, force: bool = False) -> None:
        """Create the directory structure and files for a day.

        Args:
            force: Overwrite existing files if True
        """
        if self.day_dir.exists() and not force:
            console.print(
                f"[yellow]Directory {self.day_dir} already exists. Use --force to overwrite.[/yellow]"
            )
            return

        # Create directory
        self.day_dir.mkdir(parents=True, exist_ok=True)

        # Create files
        self._create_file("__init__.py", INIT_TEMPLATE, force)
        self._create_file("solution.py", SOLUTION_TEMPLATE, force)
        self._create_file("README.md", README_TEMPLATE, force)
        self._create_file("input.txt", "", force)
        self._create_file("test_input.txt", "", force)

        console.print(
            f"[green]Created scaffold for day {self.day} at {self.day_dir}[/green]"
        )

    def _create_file(self, filename: str, template: str, force: bool) -> None:
        """Create a single file from a template."""
        file_path = self.day_dir / filename

        if file_path.exists() and not force:
            console.print(f"[yellow]  Skipping {filename} (already exists)[/yellow]")
            return

        content = template.format(day=self.day, year=self.year)
        file_path.write_text(content)
        console.print(f"[green]  Created {filename}[/green]")

    def get_solution_path(self) -> Path:
        """Get the path to the solution.py file."""
        return self.day_dir / "solution.py"

    def get_input_path(self) -> Path:
        """Get the path to the input.txt file."""
        return self.day_dir / "input.txt"

    def get_test_input_path(self) -> Path:
        """Get the path to the test_input.txt file."""
        return self.day_dir / "test_input.txt"
