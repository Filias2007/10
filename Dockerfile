FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

# Data directory for SQLite volume
RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "online_store.api:app", "--host", "0.0.0.0", "--port", "8000"]
