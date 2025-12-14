"""AOC API client for downloading inputs and submitting answers."""

from datetime import UTC, datetime
from pathlib import Path
from time import sleep
from typing import Literal

import requests
from bs4 import BeautifulSoup
from rich.console import Console

from .config import settings
from .models import SubmissionResponse

console = Console()


class AOCClient:
    """Client for interacting with Advent of Code website."""

    BASE_URL = "https://adventofcode.com"

    def __init__(self, session_cookie: str | None = None, year: int = 2025):
        """Initialize AOC client."""
        self.session_cookie = session_cookie or settings.session_cookie
        self.year = year
        self.cookies = {"session": self.session_cookie}

    def _get_url(self, day: int, endpoint: str = "") -> str:
        """Get URL for a specific day and endpoint."""
        base = f"{self.BASE_URL}/{self.year}/day/{day}"
        return f"{base}/{endpoint}" if endpoint else base

    def download_input(
        self, day: int, output_path: Path | None = None, wait_for_unlock: bool = False
    ) -> str:
        """Download input for a specific day.

        Args:
            day: Day number (1-25)
            output_path: Path to save input (optional)
            wait_for_unlock: Whether to wait for the puzzle to unlock

        Returns:
            The input text
        """
        if not 1 <= day <= 25:
            raise ValueError(f"Day must be between 1 and 25, got {day}")

        if not self.session_cookie:
            raise ValueError("Session cookie not set. Run 'aoc login' first.")

        if wait_for_unlock:
            self._wait_for_unlock(day)

        url = self._get_url(day, "input")

        for attempt in range(3):
            try:
                response = requests.get(url, cookies=self.cookies, timeout=10)
                response.raise_for_status()

                input_text = response.text

                if output_path:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(input_text)
                    console.print(
                        f"[green]Downloaded input for day {day} to {output_path}[/green]"
                    )

                return input_text

            except requests.RequestException as e:
                if attempt < 2:
                    console.print(
                        f"[yellow]Download failed (attempt {attempt + 1}/3), retrying...[/yellow]"
                    )
                    sleep(2)
                else:
                    raise ConnectionError(f"Failed to download input: {e}") from e

        raise ConnectionError("Failed to download input after 3 attempts")

    def submit_answer(
        self, day: int, part: Literal[1, 2], answer: int | str
    ) -> SubmissionResponse:
        """Submit an answer for a specific day and part.

        Args:
            day: Day number (1-25)
            part: Part number (1 or 2)
            answer: Answer to submit

        Returns:
            SubmissionResponse with success status and message
        """
        if not 1 <= day <= 25:
            raise ValueError(f"Day must be between 1 and 25, got {day}")

        if part not in (1, 2):
            raise ValueError(f"Part must be 1 or 2, got {part}")

        if not self.session_cookie:
            raise ValueError("Session cookie not set. Run 'aoc login' first.")

        url = self._get_url(day, "answer")
        data = {"level": part, "answer": str(answer)}

        for attempt in range(3):
            try:
                response = requests.post(
                    url, data=data, cookies=self.cookies, timeout=10
                )
                response.raise_for_status()

                return self._parse_submission_response(response.text)

            except requests.RequestException as e:
                if attempt < 2:
                    console.print(
                        f"[yellow]Submission failed (attempt {attempt + 1}/3), retrying...[/yellow]"
                    )
                    sleep(2)
                else:
                    raise ConnectionError(f"Failed to submit answer: {e}") from e

        raise ConnectionError("Failed to submit answer after 3 attempts")

    def _parse_submission_response(self, html: str) -> SubmissionResponse:
        """Parse the HTML response from submitting an answer."""
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("article")

        if not article:
            return SubmissionResponse(
                success=False, message="Could not parse response from AOC"
            )

        message = article.get_text(strip=True)

        # Determine success based on message content
        if "That's the right answer" in message:
            return SubmissionResponse(success=True, message=message)
        elif "That's not the right answer" in message:
            return SubmissionResponse(success=False, message=message)
        elif "You gave an answer too recently" in message:
            # Try to extract wait time
            import re

            wait_match = re.search(r"(\d+)s", message)
            wait_time = int(wait_match.group(1)) if wait_match else None
            return SubmissionResponse(
                success=False, message=message, wait_time=wait_time
            )
        elif "Did you already complete it" in message:
            return SubmissionResponse(success=False, message=message)
        else:
            return SubmissionResponse(success=False, message=message)

    def _wait_for_unlock(self, day: int) -> None:
        """Wait until the puzzle unlocks (midnight EST on the given day)."""
        # AOC puzzles unlock at midnight EST (UTC-5)
        unlock_time = datetime(self.year, 12, day, 5, 0, 0, tzinfo=UTC)
        now = datetime.now(UTC)

        if now >= unlock_time:
            return

        wait_seconds = (unlock_time - now).total_seconds()
        console.print(
            f"[yellow]Waiting {int(wait_seconds)} seconds for day {day} to unlock...[/yellow]"
        )

        while datetime.now(UTC) < unlock_time:
            remaining = (unlock_time - datetime.now(UTC)).total_seconds()
            if remaining <= 0:
                break
            console.print(
                f"\r[yellow]{int(remaining)} seconds remaining...[/yellow]", end=""
            )
            sleep(1)

        console.print("\n[green]Puzzle unlocked![/green]")

    def verify_session(self) -> bool:
        """Verify that the session cookie is valid."""
        if not self.session_cookie:
            return False

        try:
            # Try to access the settings page which requires auth
            url = f"{self.BASE_URL}/{self.year}/settings"
            response = requests.get(url, cookies=self.cookies, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False
