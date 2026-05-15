from app.models.cart import CartStatus, Workflow
from app.services.cart_service import CartService


def test_cart_service_adds_and_reviews_mock_items() -> None:
    service = CartService()

    cart = service.create_cart(Workflow.instamart)
    cart = service.add_item(cart.cart_id, "im-milk", 2)
    cart = service.review_cart(cart.cart_id)

    assert cart.status == CartStatus.reviewed
    assert cart.items[0].quantity == 2
    assert cart.subtotal == 136
    assert cart.total == 175


def test_prepare_cart_from_food_intent() -> None:
    from app.services.intent_service import IntentService

    intent = IntentService().parse("Find healthy dinner options under ₹300")
    cart = CartService().prepare_cart_from_intent(intent)

    assert cart.workflow == Workflow.food
    assert cart.items
    assert cart.mock is True
