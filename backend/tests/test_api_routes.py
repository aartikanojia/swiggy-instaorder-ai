from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_assistant_prepares_mock_cart() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"message": "Add milk, eggs, bread, and fruits to my Instamart cart."},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["requires_confirmation"] is True
    assert payload["cart"]["source"] == "mock"


def test_checkout_requires_confirmation() -> None:
    create_response = client.post("/api/v1/cart", json={"user_id": "user-1"})
    cart_id = create_response.json()["cart_id"]
    client.post(
        f"/api/v1/cart/{cart_id}/items",
        json={"item_id": "food-paneer-bowl", "item_type": "food", "quantity": 1},
    )

    checkout_response = client.post(
        "/api/v1/orders/checkout",
        json={"cart_id": cart_id, "user_confirmation": False},
    )

    assert checkout_response.status_code == 403


def test_food_search_filters() -> None:
    response = client.get(
        "/api/v1/food/search",
        params={"query": "thali", "budget": 250, "cuisine": "Indian", "veg_only": True},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload
    assert payload[0]["id"] == "food-veg-thali"
    assert payload[0]["source"] == "mock"


def test_instamart_search_filters() -> None:
    response = client.get(
        "/api/v1/instamart/search",
        params={"query": "milk", "category": "Dairy", "max_price": 80},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload
    assert payload[0]["id"] == "im-milk"
    assert payload[0]["source"] == "mock"
