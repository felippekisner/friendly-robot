from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


food_suppliers = Table(
    "food_suppliers",
    Base.metadata,
    Column("food_id", ForeignKey("foods.id"), primary_key=True),
    Column("supplier_id", ForeignKey("suppliers.id"), primary_key=True),
)


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    donated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    suppliers: Mapped[list["Supplier"]] = relationship(
        secondary=food_suppliers,
        back_populates="foods",
    )
    prices: Mapped[list["FoodPrice"]] = relationship(
        back_populates="food",
        cascade="all, delete-orphan",
    )


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    contact: Mapped[str | None] = mapped_column(String(120), nullable=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    foods: Mapped[list[Food]] = relationship(
        secondary=food_suppliers,
        back_populates="suppliers",
    )


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class FoodPrice(Base):
    __tablename__ = "food_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    effective_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    food: Mapped[Food] = relationship(back_populates="prices")
