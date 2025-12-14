"""Solution for Advent of Code 2025 - Day 3."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 3."""

    day = 3
    year = 2025

    def part_1(self) -> int | str:
        """Solve part 1."""
        total = 0
        for bank in self.input_lines:
            # Parse each line
            bank_joltage = self.joltage_of(bank, 2)
            total += bank_joltage

        return total

    def joltage_of(self, bank: str, num_batteries_to_combine: int) -> int:
        """Get the joltage of a battery given its string representation."""
        batteries = [int(joltage) for joltage in bank]
        selected_batteries: list[int] = []
        num_batteries = len(batteries)
        remaining_batteries_to_select = num_batteries - num_batteries_to_combine

        for battery_size in batteries:
            # Pop while there's a better battery coming
            while (
                selected_batteries
                and remaining_batteries_to_select > 0
                and battery_size > selected_batteries[-1]
            ):
                selected_batteries.pop()
                remaining_batteries_to_select -= 1
            selected_batteries.append(battery_size)

        # drop remaining from the end to get the target battery size
        while remaining_batteries_to_select > 0 and selected_batteries:
            selected_batteries.pop()
            remaining_batteries_to_select -= 1

        # combine the selected batteries into a joltage number
        joltage = 0
        for d in selected_batteries:
            joltage = joltage * 10 + d

        return joltage

    def part_2(self) -> int | str:
        """Solve part 2."""
        total = 0
        for bank in self.input_lines:
            # Parse each line
            bank_joltage = self.joltage_of(bank, 12)
            total += bank_joltage

        return total


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
