"""FastAPI application — Online Store REST API."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from online_store.config import get_settings
from online_store.database import get_db, init_db
from online_store.models import (
    HealthResponse,
    ProductCreate,
    ProductRead,
    PurchaseRequest,
)
from online_store.services import (
    add_product,
    filter_by_category,
    get_product,
    list_products,
    most_expensive,
    purchase,
    total_stock_value,
)

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("%s started (env=%s)", settings.app_name, settings.environment)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Online store REST API (products, categories, purchase)",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Health check endpoint for Docker / load balancers."""
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        app_name=settings.app_name,
    )


@app.post("/products", response_model=ProductRead, status_code=201, tags=["products"])
def create_product(data: ProductCreate, db: Session = Depends(get_db)) -> ProductRead:
    product = add_product(db, data)
    return ProductRead.model_validate(product)


@app.get("/products", response_model=list[ProductRead], tags=["products"])
def get_products(limit: int = 100, db: Session = Depends(get_db)) -> list[ProductRead]:
    items = list_products(db, limit=limit)
    return [ProductRead.model_validate(p) for p in items]


@app.get("/products/{product_id}", response_model=ProductRead, tags=["products"])
def get_one_product(product_id: int, db: Session = Depends(get_db)) -> ProductRead:
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead.model_validate(product)


@app.get(
    "/categories/{category}/products",
    response_model=list[ProductRead],
    tags=["categories"],
)
def products_by_category(
    category: str, db: Session = Depends(get_db)
) -> list[ProductRead]:
    items = filter_by_category(db, category)
    return [ProductRead.model_validate(p) for p in items]


@app.get("/stock/value", tags=["stock"])
def stock_value(db: Session = Depends(get_db)) -> dict[str, float]:
    return {"total_value": total_stock_value(db)}


@app.get(
    "/products/most-expensive",
    response_model=ProductRead | None,
    tags=["products"],
)
def get_most_expensive(db: Session = Depends(get_db)) -> ProductRead | None:
    product = most_expensive(db)
    if product is None:
        return None
    return ProductRead.model_validate(product)


@app.post(
    "/products/{product_id}/purchase",
    response_model=ProductRead,
    tags=["products"],
)
def purchase_product(
    product_id: int,
    body: PurchaseRequest,
    db: Session = Depends(get_db),
) -> ProductRead:
    try:
        product = purchase(db, product_id, body.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ProductRead.model_validate(product)
