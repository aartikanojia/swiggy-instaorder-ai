import pytest

from app.models.cart import CartItemType
from app.services.cart_service import CartService


def test_cart_creation() -> None:
    service = CartService()
    cart = service.create_cart("user-1")

    assert cart.user_id == "user-1"
    assert cart.items == []
    assert cart.source == "mock"


def test_adding_food_item() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    cart = service.add_item_to_cart(cart.cart_id, "food-paneer-bowl", CartItemType.food, 2)

    assert cart.item_count == 2
    assert cart.items[0].item_type == CartItemType.food


def test_adding_instamart_item() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    cart = service.add_item_to_cart(cart.cart_id, "im-milk", CartItemType.instamart, 1)

    assert cart.item_count == 1
    assert cart.items[0].item_type == CartItemType.instamart


def test_updating_quantity() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    cart = service.add_item_to_cart(cart.cart_id, "im-milk", CartItemType.instamart, 1)
    cart = service.update_item_quantity(cart.cart_id, "im-milk", 3)

    assert cart.items[0].quantity == 3
    assert cart.item_count == 3


def test_removing_item() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    cart = service.add_item_to_cart(cart.cart_id, "im-milk", CartItemType.instamart, 1)
    cart = service.remove_item_from_cart(cart.cart_id, "im-milk")

    assert cart.items == []
    assert cart.item_count == 0


def test_reviewing_cart_subtotal() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    service.add_item_to_cart(cart.cart_id, "im-milk", CartItemType.instamart, 2)
    review = service.review_cart(cart.cart_id)

    assert review.subtotal == 136
    assert review.item_count == 2


def test_clearing_cart() -> None:
    service = CartService()
    cart = service.create_cart("user-1")
    service.add_item_to_cart(cart.cart_id, "im-milk", CartItemType.instamart, 2)
    cart = service.clear_cart(cart.cart_id)

    assert cart.items == []
    assert cart.subtotal == 0


def test_invalid_cart_id_handling() -> None:
    service = CartService()
    with pytest.raises(ValueError, match="Unknown cart"):
        service.review_cart("invalid-cart")


def test_invalid_item_id_handling() -> None:
    service = CartService()
    cart = service.create_cart("user-1")

    with pytest.raises(ValueError, match="Unknown mock item"):
        service.add_item_to_cart(cart.cart_id, "bad-item", CartItemType.food, 1)


def test_invalid_item_type_handling() -> None:
    service = CartService()
    cart = service.create_cart("user-1")

    with pytest.raises(ValueError, match="Unsupported item_type"):
        service.add_item_to_cart(cart.cart_id, "im-milk", "unknown", 1)  # type: ignore[arg-type]
