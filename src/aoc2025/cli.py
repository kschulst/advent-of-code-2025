"""CLI for Advent of Code 2025 using Typer."""

import importlib.util
import sys
from pathlib import Path
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console
from rich.table import Table

from .api import AOCClient
from .config import settings
from .scaffold import DayScaffold

app = typer.Typer(
    name="aoc",
    help="Advent of Code 2025 CLI - Manage solutions, download inputs, and submit answers",
    add_completion=False,
)

console = Console()


@app.command()
def login(
    session: Annotated[
        str,
        typer.Option(
            "--session",
            "-s",
            help="AOC session cookie (or set AOC_SESSION_COOKIE env var)",
            prompt="Enter your AOC session cookie",
            hide_input=True,
        ),
    ],
) -> None:
    """Login by saving your AOC session cookie.

    To get your session cookie:
    1. Go to https://adventofcode.com
    2. Log in
    3. Open browser dev tools (F12)
    4. Go to Application/Storage > Cookies
    5. Copy the value of the 'session' cookie
    """
    settings.save_session(session)
    console.print("[green]Session cookie saved successfully![/green]")

    # Verify the session
    client = AOCClient(session)
    if client.verify_session():
        console.print("[green]Session verified! You're ready to go.[/green]")
    else:
        console.print(
            "[yellow]Warning: Could not verify session. Please check your cookie.[/yellow]"
        )


@app.command()
def new(
    day: Annotated[int, typer.Argument(help="Day number (1-25)")],
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Overwrite existing files")
    ] = False,
    download: Annotated[
        bool,
        typer.Option("--download/--no-download", "-d", help="Download input after creating scaffold"),
    ] = True,
) -> None:
    """Create a new day's solution scaffold.

    Creates directory structure with solution template, input files, and README.
    """
    scaffold = DayScaffold(day)
    scaffold.create(force=force)

    if download:
        try:
            client = AOCClient()
            input_path = scaffold.get_input_path()
            client.download_input(day, output_path=input_path)
        except Exception as e:
            console.print(f"[yellow]Could not download input: {e}[/yellow]")
            console.print("[yellow]Run 'aoc download {day}' to try again[/yellow]")


@app.command()
def download(
    day: Annotated[int, typer.Argument(help="Day number (1-25)")],
    output: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output file path"),
    ] = None,
    wait: Annotated[
        bool, typer.Option("--wait", "-w", help="Wait for puzzle to unlock")
    ] = False,
) -> None:
    """Download input for a specific day.

    If no output path is provided, saves to solutions/day_XX/input.txt
    """
    client = AOCClient()

    if output is None:
        scaffold = DayScaffold(day)
        output = scaffold.get_input_path()

    try:
        client.download_input(day, output_path=output, wait_for_unlock=wait)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def run(
    day: Annotated[int, typer.Argument(help="Day number (1-25)")],
    part: Annotated[
        Optional[int], typer.Option("--part", "-p", help="Part to run (1 or 2)")
    ] = None,
    test: Annotated[
        bool, typer.Option("--test", "-t", help="Use test_input.txt instead of input.txt")
    ] = False,
) -> None:
    """Run solution for a specific day and part."""
    scaffold = DayScaffold(day)
    solution_path = scaffold.get_solution_path()

    if not solution_path.exists():
        console.print(
            f"[red]Solution file not found: {solution_path}[/red]"
        )
        console.print(f"[yellow]Run 'aoc new {day}' to create it[/yellow]")
        raise typer.Exit(code=1)

    # Load the solution module dynamically
    spec = importlib.util.spec_from_file_location(f"day_{day:02d}.solution", solution_path)
    if spec is None or spec.loader is None:
        console.print("[red]Could not load solution module[/red]")
        raise typer.Exit(code=1)

    module = importlib.util.module_from_spec(spec)
    sys.modules[f"day_{day:02d}.solution"] = module
    spec.loader.exec_module(module)

    Solution = module.Solution

    # Get input file
    input_path = scaffold.get_test_input_path() if test else scaffold.get_input_path()

    if not input_path.exists():
        console.print(f"[red]Input file not found: {input_path}[/red]")
        raise typer.Exit(code=1)

    # Run solution
    solution = Solution.from_file(input_path)

    if part is None or part == 1:
        console.print(f"[cyan]Day {day} - Part 1:[/cyan]")
        result = solution.part_1()
        console.print(f"[green]Answer: {result}[/green]")

    if part is None or part == 2:
        console.print(f"[cyan]Day {day} - Part 2:[/cyan]")
        result = solution.part_2()
        console.print(f"[green]Answer: {result}[/green]")


@app.command()
def submit(
    day: Annotated[int, typer.Argument(help="Day number (1-25)")],
    part: Annotated[int, typer.Argument(help="Part number (1 or 2)", min=1, max=2)],
    answer: Annotated[
        Optional[str],
        typer.Option("--answer", "-a", help="Answer to submit (or use solution output)"),
    ] = None,
) -> None:
    """Submit an answer for a specific day and part.

    If no answer is provided, runs the solution and submits the result.
    """
    # Validate and narrow type for part
    if part not in (1, 2):
        console.print("[red]Part must be 1 or 2[/red]")
        raise typer.Exit(code=1)

    # Type narrowing: after the check above, part is guaranteed to be 1 or 2
    part_literal: Literal[1, 2] = part  # type: ignore[assignment]

    if answer is None:
        # Run the solution to get the answer
        scaffold = DayScaffold(day)
        solution_path = scaffold.get_solution_path()

        if not solution_path.exists():
            console.print(f"[red]Solution file not found: {solution_path}[/red]")
            raise typer.Exit(code=1)

        spec = importlib.util.spec_from_file_location(
            f"day_{day:02d}.solution", solution_path
        )
        if spec is None or spec.loader is None:
            console.print("[red]Could not load solution module[/red]")
            raise typer.Exit(code=1)

        module = importlib.util.module_from_spec(spec)
        sys.modules[f"day_{day:02d}.solution"] = module
        spec.loader.exec_module(module)

        Solution = module.Solution
        input_path = scaffold.get_input_path()

        if not input_path.exists():
            console.print(f"[red]Input file not found: {input_path}[/red]")
            raise typer.Exit(code=1)

        solution = Solution.from_file(input_path)
        answer = str(solution.part_1() if part == 1 else solution.part_2())
        console.print(f"[cyan]Submitting answer: {answer}[/cyan]")

    client = AOCClient()

    try:
        response = client.submit_answer(day, part_literal, answer)

        if response.success:
            console.print(f"[green]{response.message}[/green]")
        else:
            console.print(f"[red]{response.message}[/red]")
            if response.wait_time:
                console.print(
                    f"[yellow]Please wait {response.wait_time} seconds before submitting again[/yellow]"
                )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def status() -> None:
    """Show status of solutions and configuration."""
    table = Table(title="AOC 2025 Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    # Check session
    session_status = "✓ Set" if settings.session_cookie else "✗ Not set"
    table.add_row("Session Cookie", session_status)
    table.add_row("Year", str(settings.year))
    table.add_row("Solutions Directory", str(settings.solutions_dir))
    table.add_row("Config File", str(settings.config_file))

    console.print(table)

    # Show created days
    if settings.solutions_dir.exists():
        days = sorted(
            [
                int(d.name.split("_")[1])
                for d in settings.solutions_dir.iterdir()
                if d.is_dir() and d.name.startswith("day_")
            ]
        )

        if days:
            console.print(f"\n[cyan]Created days:[/cyan] {', '.join(map(str, days))}")
        else:
            console.print("\n[yellow]No days created yet[/yellow]")


if __name__ == "__main__":
    app()
