"""Solution for Advent of Code 2025 - Day 2."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 2."""

    day = 2
    year = 2025

    def parse_ranges(self) -> list[tuple[int, int]]:
        """Parse 'a-b,c-d,...' into a list of ranges."""
        ranges = []
        for r in self.raw_input.strip().split(","):
            start_s, end_s = r.split("-")
            ranges.append((int(start_s), int(end_s)))
        return ranges

    def part_1(self) -> int | str:
        """Solve part 1."""
        total = 0
        for start, end in self.parse_ranges():
            for num in range(start, end + 1):
                if self.has_identical_halves(num):
                    print(f"Invalid ID: {num}")
                    total += num

        return total

    def has_identical_halves(self, num: int) -> bool:
        """Check if the given ID number consists of two identical halves."""
        s = str(num)
        n = len(s)
        # Check if length is even
        if n % 2 != 0:
            return False
        half = n // 2
        return s[half:] == s[:half]

    # -------------------------------------------------------------------------

    def part_2(self) -> int | str:
        """Solve part 2."""
        total = 0
        for start, end in self.parse_ranges():
            for num in range(start, end + 1):
                if self.has_repeating_patterns(num, start, end):
                    print(f"Invalid ID: {num}")
                    total += num

        return total

    def has_repeating_patterns(self, num: int, start: int, end: int) -> bool:
        """Check if the given ID number consists of two or more repeating patterns."""
        s = str(num)
        n = len(s)
        patterns = []
        for k in range(1, n + 1):
            p = s[:k]
            number_of_repeats = n // k
            if p * number_of_repeats == s:
                if number_of_repeats > 1 and num in range(start, end + 1):
                    patterns.append(p)

        return len(patterns) > 0


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
