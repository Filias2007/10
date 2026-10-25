"""Business logic for products and purchases."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from online_store.models import ProductCreate, ProductORM


def add_product(db: Session, data: ProductCreate) -> ProductORM:
    product = ProductORM(
        name=data.name,
        category=data.category,
        price=data.price,
        quantity=data.quantity,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, limit: int = 100) -> list[ProductORM]:
    return list(db.scalars(select(ProductORM).limit(limit)).all())


def get_product(db: Session, product_id: int) -> ProductORM | None:
    return db.get(ProductORM, product_id)


def filter_by_category(db: Session, category: str) -> list[ProductORM]:
    stmt = select(ProductORM).where(ProductORM.category == category)
    return list(db.scalars(stmt).all())


def total_stock_value(db: Session) -> float:
    products = list(db.scalars(select(ProductORM)).all())
    return sum(p.price * p.quantity for p in products)


def most_expensive(db: Session) -> ProductORM | None:
    products = list(db.scalars(select(ProductORM)).all())
    if not products:
        return None
    return max(products, key=lambda p: p.price)


def purchase(db: Session, product_id: int, qty: int) -> ProductORM:
    product = db.get(ProductORM, product_id)
    if product is None:
        raise ValueError("Product not found")
    if product.quantity < qty:
        raise ValueError("Insufficient stock")
    product.quantity -= qty
    db.commit()
    db.refresh(product)
    return product
