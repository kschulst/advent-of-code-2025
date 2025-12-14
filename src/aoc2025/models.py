"""Pydantic models for AOC toolkit."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for AOC."""

    session_cookie: str = Field(default="", description="AOC session cookie")
    year: int = Field(default=2025, description="Year for AOC")
    input_dir: Path = Field(
        default=Path("solutions"), description="Directory for solutions"
    )

    class Config:
        """Pydantic config."""

        validate_assignment = True


class SubmissionResponse(BaseModel):
    """Response from submitting an answer."""

    success: bool
    message: str
    wait_time: int | None = None


class DayInfo(BaseModel):
    """Information about a specific day."""

    day: int = Field(..., ge=1, le=25)
    year: int = Field(default=2025)
    title: str | None = None
    input_path: Path | None = None
    solution_path: Path | None = None


class SolutionBase(ABC, BaseModel):
    """Base class for all day solutions using Pydantic."""

    day: ClassVar[int]
    year: ClassVar[int] = 2025

    raw_input: str = Field(default="", description="Raw input text")
    input_lines: list[str] = Field(
        default_factory=list, description="Input split into lines"
    )

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def model_post_init(self, __context: Any) -> None:
        """Initialize after model creation."""
        if self.raw_input and not self.input_lines:
            self.input_lines = self.raw_input.strip().split("\n")

    @classmethod
    def from_file(cls, file_path: Path) -> "SolutionBase":
        """Load solution from input file."""
        raw_input = file_path.read_text()
        return cls(raw_input=raw_input)

    @abstractmethod
    def part_1(self) -> int | str:
        """Solve part 1."""
        raise NotImplementedError

    @abstractmethod
    def part_2(self) -> int | str:
        """Solve part 2."""
        raise NotImplementedError
