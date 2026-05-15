import pytest

from app.models.cart import Cart, CartItem, Workflow
from app.services.policy_service import PolicyError, PolicyService


def test_checkout_requires_user_confirmation() -> None:
    cart = Cart(
        cart_id="cart-1",
        workflow=Workflow.food,
        items=[CartItem(item_id="item-1", name="Mock item", quantity=1, unit_price=100)],
    )

    with pytest.raises(PolicyError):
        PolicyService().validate_checkout(cart, user_confirmation=False)


def test_checkout_allows_confirmed_mock_cart() -> None:
    cart = Cart(
        cart_id="cart-1",
        workflow=Workflow.food,
        items=[CartItem(item_id="item-1", name="Mock item", quantity=1, unit_price=100)],
    )

    PolicyService().validate_checkout(cart, user_confirmation=True)
