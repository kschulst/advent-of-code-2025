"""Solution for Advent of Code 2025 - Day 4."""

from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 4."""

    day = 4
    year = 2025

    def part_1(self) -> int | str:
        """Solve part 1."""
        grid = [list(line) for line in self.input_lines]
        coords = self.coordinates_with_less_than_four_neighbors(grid)
        return len(coords)

    def part_2(self) -> int | str:
        """Solve part 2."""
        grid = [list(line) for line in self.input_lines]

        total_remove_count = 0
        remove_count = -1
        while remove_count != 0:
            print("-------------------------------------")
            self.print_grid(grid)
            coords_to_remove = self.coordinates_with_less_than_four_neighbors(grid)
            remove_count = len(coords_to_remove)
            print(f"Removing {remove_count} rolls of paper...")
            grid = self.remove_rolls_from_grid(grid, coords_to_remove)
            total_remove_count += remove_count

        return total_remove_count

    def coordinates_with_less_than_four_neighbors(
        self, grid: list[list[str]]
    ) -> list[tuple[int, int]]:
        """Find coordinates with less than four neighboring '@' characters."""
        # grid[row][col]
        height, width = len(grid), len(grid[0])

        # Possible directions to check neighbors
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        coordinates_with_less_than_four_neighbors = []
        for y in range(height):
            for x in range(width):
                # Only consider coordinates with a roll of paper ('@')
                if grid[y][x] == "@":
                    neighbor_count = 0
                    for dy, dx in dirs:
                        ny = y + dy
                        nx = x + dx
                        # Check bounds and if neighbor is "@"
                        if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] == "@":
                            neighbor_count += 1

                    if neighbor_count < 4:
                        coordinates_with_less_than_four_neighbors.append((x, y))

        return coordinates_with_less_than_four_neighbors

    def remove_rolls_from_grid(
        self, grid: list[list[str]], coords_of_rolls_to_remove: list[tuple[int, int]]
    ) -> list[list[str]]:
        """Remove rolls of paper from the grid at specified coordinates."""
        for x, y in coords_of_rolls_to_remove:
            grid[y][x] = "."
        return grid

    def print_grid(self, grid: list[list[str]]) -> None:
        """Print the grid to the console."""
        height, width = len(grid), len(grid[0])
        print(f"Grid size {width}x{height}")
        for row in grid:
            print("".join(row))


if __name__ == "__main__":
    # For quick testing
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    solution = Solution.from_file(input_file)

    print(f"Part 1: {solution.part_1()}")
    print(f"Part 2: {solution.part_2()}")
