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
    assert payload["cart"]["mock"] is True
    assert payload["cart"]["workflow"] == "instamart"


def test_checkout_requires_confirmation() -> None:
    create_response = client.post("/api/v1/cart", json={"workflow": "food"})
    cart_id = create_response.json()["cart_id"]
    client.post(f"/api/v1/cart/{cart_id}/items", json={"item_id": "food-snack-combo", "quantity": 1})

    checkout_response = client.post(
        "/api/v1/orders/checkout",
        json={"cart_id": cart_id, "user_confirmation": False},
    )

    assert checkout_response.status_code == 403
