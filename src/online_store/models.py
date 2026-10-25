"""SQLAlchemy models and Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ProductORM(Base):
    """SQLAlchemy product table."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


# ---------- Pydantic schemas ----------


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int

    model_config = {"from_attributes": True}


class PurchaseRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class HealthResponse(BaseModel):
    status: str
    environment: str
    app_name: str
