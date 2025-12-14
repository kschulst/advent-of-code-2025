# Kennneth's Advent of Code 2025 🎄

A Python toolkit for solving [Advent of Code](https://adventofcode.com) puzzles with a handy CLI and web showcase. Fork and use it for your own solutions! 🧑🏻‍🎄

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [CLI Commands](#cli-commands)
- [Writing Solutions](#writing-solutions)
- [Web Showcase](#web-showcase)
- [Type Safety](#type-safety)
- [Configuration](#configuration)
- [Project Structure](#project-structure)

## Quick Start

**Note**: The following assumes you've installed the tool globally with `uv tool install .` and can use `aoc` commands directly. See [Installation](#installation) for setup.

```bash
# 1. Install dependencies and tool
uv sync
uv tool install -e .

# 2. Login with your AOC session cookie
aoc login

# 3. Create a new day
aoc new 1

# 4. Edit your solution in solutions/day_01/solution.py

# 5. Run your solution
aoc run 1

# 6. Submit your answer
aoc submit 1 1  # day 1, part 1
```

## Installation

### Prerequisites
- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Clone or create your repository
git clone <this-repo>
cd aoc2025

# Install dependencies
uv sync

# Install with dev dependencies (includes pyright)
uv sync --extra dev

# Install the tool globally so you can use 'aoc' directly
uv tool install .
```

This makes the `aoc` command available globally. You can now use `aoc` instead of `uv run aoc` throughout the rest of this guide.

### Get Your Session Cookie

1. Go to https://adventofcode.com and login
2. Open browser dev tools (F12)
3. Go to Application/Storage > Cookies
4. Copy the value of the `session` cookie
5. Run `aoc login` and paste the cookie

## CLI Commands

### `aoc login`
Save your AOC session cookie for automatic input downloads and answer submissions.

```bash
aoc login
# Or with environment variable
export AOC_SESSION_COOKIE=your-cookie-here
```

### `aoc new <day>`
Create a new day's solution scaffold with all necessary files.

```bash
aoc new 1              # Create day 1 with auto-download
aoc new 2 --no-download # Create without downloading input
aoc new 3 --force      # Overwrite existing files
```

Creates:
- `solutions/day_XX/solution.py` - Solution template
- `solutions/day_XX/input.txt` - Puzzle input
- `solutions/day_XX/test_input.txt` - Test input
- `solutions/day_XX/README.md` - Notes template
- `solutions/day_XX/__init__.py` - Package init

### `aoc download <day>`
Download puzzle input for a specific day.

```bash
aoc download 1
aoc download 5 --wait   # Wait for puzzle unlock
aoc download 3 -o custom_input.txt
```

### `aoc run <day>`
Run your solution and see the answers.

```bash
aoc run 1              # Run both parts
aoc run 1 --part 1     # Run only part 1
aoc run 1 --part 2     # Run only part 2
aoc run 1 --test       # Use test_input.txt
```

### `aoc submit <day> <part>`
Submit your answer to AOC.

```bash
aoc submit 1 1         # Submit day 1, part 1
aoc submit 1 2         # Submit day 1, part 2
aoc submit 1 1 --answer 42  # Submit specific answer
```

### `aoc status`
Show configuration and progress.

```bash
aoc status
```

## Writing Solutions

### Solution Template

Every solution inherits from `SolutionBase` and implements two methods:

```python
from aoc2025.models import SolutionBase


class Solution(SolutionBase):
    """Solution for day 1."""

    day = 1
    year = 2025

    def part_1(self) -> int | str:
        """Solve part 1."""
        # Your solution here
        return 0

    def part_2(self) -> int | str:
        """Solve part 2."""
        # Your solution here
        return 0
```

### Available Properties

- `self.raw_input: str` - Full input as a single string
- `self.input_lines: list[str]` - Input split into lines
- `self.day: int` - Current day number
- `self.year: int` - Current year

### Common Patterns

#### Parse integers from lines
```python
def part_1(self) -> int | str:
    numbers = [int(line) for line in self.input_lines]
    return sum(numbers)
```

#### Parse grid
```python
def part_1(self) -> int | str:
    grid = [list(line) for line in self.input_lines]
    # grid[row][col]
    return 0
```

#### Parse grouped input
```python
def part_1(self) -> int | str:
    groups = self.raw_input.strip().split('\n\n')
    for group in groups:
        lines = group.split('\n')
        # Process group
    return 0
```

#### Add helper methods
```python
class Solution(SolutionBase):
    day = 1
    year = 2025

    def parse_data(self) -> list[tuple[int, int]]:
        """Parse input into structured data."""
        result = []
        for line in self.input_lines:
            a, b = map(int, line.split())
            result.append((a, b))
        return result

    def part_1(self) -> int | str:
        data = self.parse_data()
        # Use parsed data
        return 0
```

#### Use Pydantic models for complex parsing
```python
from pydantic import BaseModel

class Instruction(BaseModel):
    op: str
    value: int

class Solution(SolutionBase):
    day = 1
    year = 2025

    def part_1(self) -> int | str:
        instructions = []
        for line in self.input_lines:
            op, val = line.split()
            instructions.append(Instruction(op=op, value=int(val)))
        return 0
```

## Web Showcase

View all your solutions in a web interface with syntax highlighting and input visualization.

### Setup

```bash
# First time setup (creates database)
uv run python src/aoc2025/web/manage.py migrate

# Start the server
uv run python src/aoc2025/web/manage.py runserver
```

Visit http://localhost:8000

### Features

- 📊 Overview of all completed days
- 🎨 Python syntax highlighting
- 📝 Display answers for both parts
- 📄 View puzzle input (collapsible)
- 🔗 Direct links to AOC problem pages
- ⬇️ Download inputs directly from web UI

## Type Safety

This project uses **strict type checking** with pyright to ensure code quality.

### Running Type Checks

```bash
# Install dev dependencies
uv sync --extra dev

# Check all code
uv run pyright

# Check specific directories
uv run pyright src
uv run pyright solutions
```

## Configuration

### Environment Variables

```bash
export AOC_SESSION_COOKIE=your-session-cookie
export AOC_YEAR=2025
export AOC_SOLUTIONS_DIR=./solutions
```

### Config File

Located at `~/.config/aoc2025/config.yml`:

```yaml
session_cookie: your-session-cookie-here
year: 2025
```

### Priority

1. Environment variables (highest)
2. Config file
3. Default values (lowest)

## Project Structure

```
advent-of-code-2025/
├── src/aoc2025/              
│   ├── models.py             # Pydantic models (SolutionBase)
│   ├── config.py             # Settings management
│   ├── api.py                # AOC API client
│   ├── scaffold.py           # Day template generator
│   ├── cli.py                # Typer CLI commands
│   └── web/                  # Django web app
│       ├── manage.py         # Django management
│       ├── settings.py       # Django settings
│       ├── urls.py           # URL routing
│       └── showcase/         # Showcase app
│           ├── views.py      # Views with type hints
│           └── templates/    # HTML templates
├── solutions/                # Puzzle solutions
│   ├── day_01/
│   │   ├── solution.py       # Puzzle code
│   │   ├── input.txt         # Puzzle input
│   │   ├── test_input.txt    # Test data
│   │   └── README.md         # Your notes
│   ├── day_02/
│   └── ...
├── pyproject.toml            # Dependencies and pyright config
├── README.md                 # This file
└── Makefile                  # Convenience shortcuts
```

## Makefile Shortcuts

```bash
make install             # Install dependencies
make login               # Login with session cookie
make new DAY=1           # Create new day
make run DAY=1           # Run solution
make test DAY=1          # Run with test input
make submit DAY=1 PART=1 # Submit answer
make web                 # Start Django server
make check               # Run pyright type checker
```

## Example Workflow

```bash
# Morning of December 1st
aoc new 1

# Read the problem on adventofcode.com
# Edit solutions/day_01/solution.py

# Test with example input
echo "test data" > solutions/day_01/test_input.txt
aoc run 1 --test

# Run with real input
aoc run 1

# Submit part 1
aoc submit 1 1

# Solve part 2
# Edit solution.py

# Test and submit part 2
aoc run 1 --part 2
aoc submit 1 2

# View in web interface
uv run python src/aoc2025/web/manage.py runserver
```

## Troubleshooting

### Session Cookie Issues
```bash
# Verify your session is valid
aoc status

# Re-login if needed
aoc login
```

### Import Errors
```bash
# Reinstall package
uv sync

# Or rebuild
uv pip install -e .
```

### Django Database Issues
```bash
# Reset database
rm src/aoc2025/web/db.sqlite3
uv run python src/aoc2025/web/manage.py migrate
```

## Tech Stack

- **Python 3.12+** - Language
- **uv** - Package manager
- **Pydantic** - Data validation and settings
- **Typer** - CLI framework
- **Django 5.x** - Web framework
- **Rich** - Terminal formatting
- **BeautifulSoup4** - HTML parsing
- **pyright** - Type checker
- **Highlight.js** - Syntax highlighting

## License

MIT License
