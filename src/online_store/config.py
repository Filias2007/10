"""Application configuration via environment variables (no secrets in code)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from environment / .env file."""

    app_name: str = "Online Store"
    environment: str = "development"
    database_url: str = "sqlite:///./data/app.db"
    log_level: str = "INFO"
    # Optional API key — never hardcode real values
    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
