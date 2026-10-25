# Online Store

Production-oriented REST API for an online store (Laboratory work №10, variant 3).

**Package:** `online-store` / `online_store`

## Features

- Product catalog (name, category, price, quantity)
- Search / filter by category
- Total stock value
- Most expensive product
- Purchase (stock decrease)
- SQLite persistence
- Configuration via environment variables
- FastAPI + OpenAPI docs
- Docker + non-root user + HEALTHCHECK
- GitHub Actions CI (lint, mypy, tests, build, Docker)

## Requirements

- Python ≥ 3.11
- Docker (optional, for container run)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Configuration

Copy the example and edit values (never commit real secrets):

```bash
cp .env.example .env
```

| Variable        | Description              | Default                      |
|-----------------|--------------------------|------------------------------|
| `APP_NAME`      | Application title        | Online Store                 |
| `ENVIRONMENT`   | development / production | development                  |
| `DATABASE_URL`  | SQLAlchemy URL           | sqlite:///./data/app.db      |
| `LOG_LEVEL`     | Logging level            | INFO                         |
| `API_KEY`       | Optional secret key      | (empty)                      |

Secrets (passwords, tokens, API keys) must **not** appear in source code, README, Dockerfile or Git.

## Running locally

```bash
# via console script
online-store

# or uvicorn directly
uvicorn online_store.api:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://localhost:8000/health  
- Swagger: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

## API endpoints

| Method | Path                              | Description              |
|--------|-----------------------------------|--------------------------|
| GET    | `/health`                         | Health check             |
| POST   | `/products`                       | Create product           |
| GET    | `/products`                       | List products            |
| GET    | `/products/{id}`                  | Get product              |
| GET    | `/categories/{category}/products` | Filter by category       |
| GET    | `/stock/value`                    | Total stock value        |
| GET    | `/products/most-expensive`        | Most expensive product   |
| POST   | `/products/{id}/purchase`         | Purchase (reduce qty)    |

## Running with Docker

```bash
docker build -t online-store:1.0 .

docker run --rm -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  -e DATABASE_URL=sqlite:////app/data/app.db \
  -v store_data:/app/data \
  online-store:1.0
```

Then open http://localhost:8000/health

## Testing

```bash
pytest -v
ruff check .
ruff format --check .
mypy src
```

## Packaging

```bash
python -m pip install build
python -m build
# produces dist/online_store-1.0.0-py3-none-any.whl and .tar.gz
```

Install wheel in a clean environment:

```bash
python -m venv test_env && source test_env/bin/activate
pip install dist/online_store-1.0.0-py3-none-any.whl
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push/PR:

1. Ruff lint + format check  
2. mypy type check  
3. pytest  
4. `python -m build`  
5. `docker build`

## Project structure

```
LAB_10/
├── .github/workflows/ci.yml
├── src/online_store/
│   ├── api.py          # FastAPI routes
│   ├── config.py       # pydantic-settings
│   ├── database.py
│   ├── models.py
│   ├── services.py
│   └── main.py
├── tests/
├── Dockerfile
├── .dockerignore
├── .env.example
├── pyproject.toml
├── README.md
└── LICENSE
```

## Authors

Student — Laboratory course «Professional Python», 2026.
