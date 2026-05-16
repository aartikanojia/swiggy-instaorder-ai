from app.adapters import mock_swiggy_tools
from app.models.cart import Workflow


def test_mock_tools_create_review_checkout_and_track() -> None:
    cart = mock_swiggy_tools.create_cart(Workflow.food)
    cart = mock_swiggy_tools.add_item_to_cart(cart.cart_id, "food-paneer-bowl", 1)
    cart = mock_swiggy_tools.review_cart(cart.cart_id)

    assert cart.total > 0

    order = mock_swiggy_tools.confirm_checkout_mock(cart.cart_id)
    tracked = mock_swiggy_tools.track_order_mock(order.order_id)

    assert tracked.order_id == order.order_id
    assert tracked.mock is True


def test_food_search_applies_required_filters() -> None:
    results = mock_swiggy_tools.search_food(query="paneer", budget=300, cuisine="North Indian", veg_only=True)

    assert results
    assert all(item["source"] == "mock" for item in results)
    assert all(item["price"] <= 300 for item in results)
    assert all(item["cuisine"] == "North Indian" for item in results)


def test_instamart_search_applies_required_filters() -> None:
    results = mock_swiggy_tools.search_instamart_items(query="bread", category="Bakery", max_price=100)

    assert results
    assert all(item["source"] == "mock" for item in results)
    assert all(item["category"] == "Bakery" for item in results)
    assert all(item["price"] <= 100 for item in results)
