"""API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "app_name" in data


def test_create_and_list_product(client: TestClient) -> None:
    payload = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 25000.0,
        "quantity": 5,
    }
    r = client.post("/products", json=payload)
    assert r.status_code == 201
    product = r.json()
    assert product["name"] == "Laptop"
    assert product["id"] >= 1

    r2 = client.get("/products")
    assert r2.status_code == 200
    assert len(r2.json()) >= 1


def test_filter_by_category(client: TestClient) -> None:
    client.post(
        "/products",
        json={
            "name": "Phone",
            "category": "Electronics",
            "price": 10000,
            "quantity": 3,
        },
    )
    client.post(
        "/products",
        json={"name": "Book", "category": "Books", "price": 200, "quantity": 10},
    )
    r = client.get("/categories/Electronics/products")
    assert r.status_code == 200
    items = r.json()
    assert all(p["category"] == "Electronics" for p in items)


def test_purchase(client: TestClient) -> None:
    r = client.post(
        "/products",
        json={"name": "Mouse", "category": "Electronics", "price": 500, "quantity": 10},
    )
    pid = r.json()["id"]
    r2 = client.post(f"/products/{pid}/purchase", json={"quantity": 3})
    assert r2.status_code == 200
    assert r2.json()["quantity"] == 7


def test_purchase_insufficient_stock(client: TestClient) -> None:
    r = client.post(
        "/products",
        json={"name": "Rare", "category": "Toys", "price": 100, "quantity": 1},
    )
    pid = r.json()["id"]
    r2 = client.post(f"/products/{pid}/purchase", json={"quantity": 5})
    assert r2.status_code == 400


def test_stock_value(client: TestClient) -> None:
    client.post(
        "/products",
        json={"name": "Item", "category": "Home", "price": 100.0, "quantity": 2},
    )
    r = client.get("/stock/value")
    assert r.status_code == 200
    assert r.json()["total_value"] >= 200.0
