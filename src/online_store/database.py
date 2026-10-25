"""Database engine and session factory."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from online_store.config import get_settings
from online_store.models import Base

settings = get_settings()

# Ensure directory exists for SQLite file paths
if settings.database_url.startswith("sqlite"):
    # Extract path after sqlite:///
    raw = settings.database_url.replace("sqlite:///", "", 1)
    if raw and raw != ":memory:":
        Path(raw).parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
