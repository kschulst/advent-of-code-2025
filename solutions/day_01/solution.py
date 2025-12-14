"""Solution for Advent of Code 2025 - Day 1."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 1."""

    day = 1
    year = 2025

    def part_1(self) -> int | str:
        """Solve part 1."""
        current_pos = 50
        zero_count = 0

        for line in self.input_lines:
            direction = -1 if line[0] == "L" else 1
            click_count = int(line[1:])
            current_pos = (current_pos + click_count * direction) % 100
            if current_pos == 0:
                zero_count += 1

        return zero_count

    def part_2(self) -> int | str:
        """Solve part 2."""
        current_pos = 50
        pass_zero_count = 0

        for line in self.input_lines:
            direction = -1 if line[0] == "L" else 1
            click_count = int(line[1:])
            delta = click_count * direction
            start = current_pos
            end = start + delta

            # Count how many times this move crosses position 0
            if delta > 0:
                # Moving right: count multiples of 100 in the interval start to end
                # This is the number of 100-block boundaries crossed.
                pass_zero_count += end // 100 - start // 100
            elif delta < 0:
                # Moving left
                # Using ceiling-division gives the count of 100-block boundaries when moving backwards.
                pass_zero_count += self.ceil_div(start, 100) - self.ceil_div(end, 100)

            current_pos = end % 100

        return pass_zero_count

    def ceil_div(self, a: int, m: int) -> int:
        """Return the ceiling of a divided by m."""
        return -((-a) // m)


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
