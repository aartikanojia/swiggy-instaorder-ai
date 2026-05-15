from app.adapters import mock_swiggy_tools
from app.models.cart import Workflow


def test_mock_tools_create_review_checkout_and_track() -> None:
    cart = mock_swiggy_tools.create_cart(Workflow.food)
    cart = mock_swiggy_tools.add_item_to_cart(cart.cart_id, "food-snack-combo", 1)
    cart = mock_swiggy_tools.review_cart(cart.cart_id)

    assert cart.total > 0

    order = mock_swiggy_tools.confirm_checkout_mock(cart.cart_id)
    tracked = mock_swiggy_tools.track_order_mock(order.order_id)

    assert tracked.order_id == order.order_id
    assert tracked.mock is True
