"""Configuration management for AOC 2025."""

from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AOC_",
        case_sensitive=False,
    )

    session_cookie: str = ""
    year: int = 2025
    solutions_dir: Path = Path(__file__).parent.parent.parent / "solutions"
    config_file: Path = Path.home() / ".config" / "aoc2025" / "config.yml"

    def model_post_init(self, __context: Any) -> None:
        """Load config file after initialization if env vars not set."""
        # Only load from file if session_cookie wasn't set by env var
        if not self.session_cookie:
            self.load_session()

    def ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

    def save_session(self, session: str) -> None:
        """Save session cookie to config file."""
        self.session_cookie = session
        self.ensure_config_dir()

        import yaml

        config_data = {"session_cookie": session, "year": self.year}

        with self.config_file.open("w") as f:
            yaml.safe_dump(config_data, f)

    def load_session(self) -> str:
        """Load session cookie from config file."""
        if self.config_file.exists():
            import yaml

            with self.config_file.open("r") as f:
                config_data = yaml.safe_load(f)
                self.session_cookie = config_data.get("session_cookie", "")

        return self.session_cookie


# Global settings instance
settings = Settings()
