"""Solution for Advent of Code 2025 - Day 5."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 5."""

    day = 5
    year = 2025

    def part_1(self) -> int | str:
        """Solve part 1."""
        ingredient_ranges = self.ingredient_ranges()
        available_ingredients = self.available_ingredients()

        spoiled = []
        for ingredient in available_ingredients:
            if self.in_any_range(ingredient, ingredient_ranges):
                spoiled.append(ingredient)

        num_spoiled = len(spoiled)
        return num_spoiled

    def part_2(self) -> int | str:
        """Solve part 2."""
        ingredient_ranges = self.ingredient_ranges()
        merged_ranges = self.merge_overlapping_ranges(ingredient_ranges)
        print(f"Merged ranges: {merged_ranges}")
        count = 0
        for start, end in merged_ranges:
            count += end - start + 1

        return count

    def ingredient_ranges(self) -> list[tuple[int, int]]:
        groups = self.raw_input.strip().split("\n\n")
        ingredient_ranges_input = groups[0].splitlines()
        ingredient_ranges: list[tuple[int, int]] = [
            tuple(map(int, s.split("-"))) for s in ingredient_ranges_input
        ]
        return ingredient_ranges

    def available_ingredients(self) -> list[int]:
        groups = self.raw_input.strip().split("\n\n")
        available_ingredients_input = groups[1].splitlines()
        available_ingredients = [
            int(ingredient) for ingredient in available_ingredients_input
        ]
        return available_ingredients

    def in_any_range(self, n: int, ranges: list[tuple[int, int]]) -> bool:
        """Check if number is in any of the given ranges."""
        return any(a <= n <= b for a, b in ranges)

    def merge_overlapping_ranges(
        self, ranges: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Merge overlapping ranges into non-overlapping ranges."""
        if not ranges:
            return []

        # Sort ranges by start value
        sorted_ranges = sorted(ranges)
        merged_ranges = [sorted_ranges[0]]

        for current in sorted_ranges[1:]:
            last_merged = merged_ranges[-1]
            # Check if overlap
            if current[0] <= last_merged[1]:
                # Merge the ranges
                merged_ranges[-1] = (
                    last_merged[0],
                    max(last_merged[1], current[1]),
                )
            else:
                merged_ranges.append(current)

        return merged_ranges


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
