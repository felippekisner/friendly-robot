from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

try:
    from src.database import SessionLocal
    from src.models import Food, FoodPrice, Supplier, Worker
except ModuleNotFoundError:
    from database import SessionLocal
    from models import Food, FoodPrice, Supplier, Worker


def get_db_session() -> Session:
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise


def create_food(data: dict, supplier_ids: Iterable[int] | None = None) -> Food:
    session = get_db_session()
    food = Food(**data)
    if supplier_ids:
        suppliers = session.execute(select(Supplier).where(Supplier.id.in_(list(supplier_ids)))).scalars().all()
        food.suppliers = suppliers
    session.add(food)
    session.commit()
    session.refresh(food)
    session.close()
    return food


def list_foods() -> list[Food]:
    session = get_db_session()
    foods = session.execute(
        select(Food).options(selectinload(Food.suppliers))
    ).scalars().all()
    session.close()
    return foods


def update_food(food_id: int, data: dict, supplier_ids: Iterable[int] | None = None) -> Food | None:
    session = get_db_session()
    food = session.get(Food, food_id)
    if not food:
        session.close()
        return None

    for key, value in data.items():
        setattr(food, key, value)

    if supplier_ids is not None:
        suppliers = session.execute(select(Supplier).where(Supplier.id.in_(list(supplier_ids)))).scalars().all()
        food.suppliers = suppliers

    session.commit()
    session.refresh(food)
    session.close()
    return food


def delete_food(food_id: int) -> bool:
    session = get_db_session()
    food = session.get(Food, food_id)
    if not food:
        session.close()
        return False
    session.delete(food)
    session.commit()
    session.close()
    return True


def create_supplier(data: dict) -> Supplier:
    session = get_db_session()
    supplier = Supplier(**data)
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    session.close()
    return supplier


def list_suppliers() -> list[Supplier]:
    session = get_db_session()
    suppliers = session.execute(
        select(Supplier).options(selectinload(Supplier.foods))
    ).scalars().all()
    session.close()
    return suppliers


def update_supplier(supplier_id: int, data: dict) -> Supplier | None:
    session = get_db_session()
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        session.close()
        return None

    for key, value in data.items():
        setattr(supplier, key, value)

    session.commit()
    session.refresh(supplier)
    session.close()
    return supplier


def delete_supplier(supplier_id: int) -> bool:
    session = get_db_session()
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        session.close()
        return False
    session.delete(supplier)
    session.commit()
    session.close()
    return True


def create_worker(data: dict) -> Worker:
    session = get_db_session()
    worker = Worker(**data)
    session.add(worker)
    session.commit()
    session.refresh(worker)
    session.close()
    return worker


def list_workers() -> list[Worker]:
    session = get_db_session()
    workers = session.execute(select(Worker)).scalars().all()
    session.close()
    return workers


def update_worker(worker_id: int, data: dict) -> Worker | None:
    session = get_db_session()
    worker = session.get(Worker, worker_id)
    if not worker:
        session.close()
        return None

    for key, value in data.items():
        setattr(worker, key, value)

    session.commit()
    session.refresh(worker)
    session.close()
    return worker


def delete_worker(worker_id: int) -> bool:
    session = get_db_session()
    worker = session.get(Worker, worker_id)
    if not worker:
        session.close()
        return False
    session.delete(worker)
    session.commit()
    session.close()
    return True


def create_price(data: dict) -> FoodPrice:
    session = get_db_session()
    price = FoodPrice(**data)
    session.add(price)
    session.commit()
    session.refresh(price)
    session.close()
    return price


def list_prices() -> list[FoodPrice]:
    session = get_db_session()
    prices = session.execute(
        select(FoodPrice).options(selectinload(FoodPrice.food))
    ).scalars().all()
    session.close()
    return prices


def update_price(price_id: int, data: dict) -> FoodPrice | None:
    session = get_db_session()
    price = session.get(FoodPrice, price_id)
    if not price:
        session.close()
        return None

    for key, value in data.items():
        setattr(price, key, value)

    session.commit()
    session.refresh(price)
    session.close()
    return price


def delete_price(price_id: int) -> bool:
    session = get_db_session()
    price = session.get(FoodPrice, price_id)
    if not price:
        session.close()
        return False
    session.delete(price)
    session.commit()
    session.close()
    return True
