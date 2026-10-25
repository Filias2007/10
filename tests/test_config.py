"""Configuration tests."""

from __future__ import annotations

from online_store.config import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.environment in {"development", "test", "production"}
    assert s.app_name
    assert s.log_level
    assert "sqlite" in s.database_url or s.database_url


def test_settings_from_env(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("APP_NAME", "Test Store")
    # Clear cache of get_settings if needed — create fresh instance
    s = Settings()
    assert s.environment == "production"
    assert s.log_level == "WARNING"
    assert s.app_name == "Test Store"
