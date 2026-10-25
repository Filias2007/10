"""CLI entry point."""

from __future__ import annotations

import uvicorn

from online_store.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "online_store.api:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
