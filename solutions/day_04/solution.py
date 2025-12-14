"""Solution for Advent of Code 2025 - Day 4."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 4."""

    day = 4
    year = 2025

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

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
