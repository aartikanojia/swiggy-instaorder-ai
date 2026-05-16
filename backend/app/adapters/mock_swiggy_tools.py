import json
from itertools import count
from pathlib import Path

from app.models.cart import Cart, CartItem, CartItemType, CartStatus, MockOrder, OrderStatus, Workflow

_cart_counter = count(1)
_order_counter = count(1)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FOOD_DATA: list[dict] = json.loads((DATA_DIR / "mock_food.json").read_text(encoding="utf-8"))
INSTAMART_DATA: list[dict] = json.loads((DATA_DIR / "mock_instamart.json").read_text(encoding="utf-8"))

FOOD_ITEMS = {item["id"]: item for item in FOOD_DATA}
INSTAMART_ITEMS = {item["id"]: item for item in INSTAMART_DATA}

CARTS: dict[str, Cart] = {}
ORDERS: dict[str, MockOrder] = {}


def search_food(
    query: str = "",
    budget: int | None = None,
    cuisine: str | None = None,
    veg_only: bool = False,
) -> list[dict]:
    terms = _to_terms(query)
    filtered = []
    for item in FOOD_DATA:
        if budget is not None and item["price"] > budget:
            continue
        if cuisine and item["cuisine"].lower() != cuisine.lower():
            continue
        if veg_only and not item["veg"]:
            continue
        if terms and not _matches_terms(item["name"], terms):
            continue
        filtered.append(
            {
                "id": item["id"],
                "name": item["name"],
                "cuisine": item["cuisine"],
                "price": item["price"],
                "availability": item["availability"],
                "source": "mock",
            }
        )
    return filtered


def search_instamart_items(
    query: str = "",
    category: str | None = None,
    max_price: int | None = None,
) -> list[dict]:
    terms = _to_terms(query)
    filtered = []
    for item in INSTAMART_DATA:
        if category and item["category"].lower() != category.lower():
            continue
        if max_price is not None and item["price"] > max_price:
            continue
        if terms and not _matches_terms(item["name"], terms):
            continue
        filtered.append(
            {
                "id": item["id"],
                "name": item["name"],
                "category": item["category"],
                "price": item["price"],
                "availability": item["availability"],
                "source": "mock",
            }
        )
    return filtered


def create_cart(user_id: str, workflow: Workflow | None = None) -> Cart:
    cart = Cart(cart_id=f"mock-cart-{next(_cart_counter)}", user_id=user_id, workflow=workflow)
    CARTS[cart.cart_id] = cart
    return cart


def add_item_to_cart(cart_id: str, item_id: str, item_type: CartItemType, quantity: int = 1) -> Cart:
    cart = _get_cart(cart_id)
    catalog_item = _catalog_item(item_id, item_type)

    existing = next(
        (cart_item for cart_item in cart.items if cart_item.item_id == item_id and cart_item.item_type == item_type),
        None,
    )
    if existing:
        existing.quantity += quantity
    else:
        cart.items.append(
            CartItem(
                item_id=item_id,
                name=catalog_item["name"],
                item_type=item_type,
                price=catalog_item["price"],
                quantity=quantity,
                availability=catalog_item["availability"],
            )
        )
    return _recalculate(cart)


def remove_item_from_cart(cart_id: str, item_id: str) -> Cart:
    cart = _get_cart(cart_id)
    filtered_items = [cart_item for cart_item in cart.items if cart_item.item_id != item_id]
    if len(filtered_items) == len(cart.items):
        raise ValueError(f"Item is not in cart: {item_id}")
    cart.items = filtered_items
    return _recalculate(cart)


def update_item_quantity(cart_id: str, item_id: str, quantity: int) -> Cart:
    cart = _get_cart(cart_id)
    existing = next((cart_item for cart_item in cart.items if cart_item.item_id == item_id), None)
    if not existing:
        raise ValueError(f"Item is not in cart: {item_id}")
    existing.quantity = quantity
    return _recalculate(cart)


def review_cart(cart_id: str) -> Cart:
    cart = _get_cart(cart_id)
    cart.status = CartStatus.reviewed
    return _recalculate(cart)


def clear_cart(cart_id: str) -> Cart:
    cart = _get_cart(cart_id)
    cart.items = []
    cart.status = CartStatus.draft
    return _recalculate(cart)


def apply_coupon_mock(cart_id: str, coupon_code: str) -> Cart:
    cart = _get_cart(cart_id)
    cart.applied_coupon = coupon_code.upper()
    return _recalculate(cart)


def confirm_checkout_mock(cart_id: str) -> MockOrder:
    cart = _get_cart(cart_id)
    cart.status = CartStatus.checked_out
    order = MockOrder(order_id=f"mock-order-{next(_order_counter)}", cart_id=cart.cart_id)
    ORDERS[order.order_id] = order
    return order


def track_order_mock(order_id: str | None = None) -> MockOrder:
    if order_id and order_id in ORDERS:
        return ORDERS[order_id].model_copy(update={"status": OrderStatus.preparing})
    if ORDERS:
        latest_order_id = next(reversed(ORDERS))
        return ORDERS[latest_order_id].model_copy(update={"status": OrderStatus.preparing})
    return MockOrder(order_id="mock-order-demo", cart_id="mock-cart-demo", status=OrderStatus.out_for_delivery)


def _catalog_item(item_id: str, item_type: CartItemType) -> dict:
    if item_type == CartItemType.food:
        if item_id not in FOOD_ITEMS:
            raise ValueError(f"Unknown mock item: {item_id}")
        return FOOD_ITEMS[item_id]

    if item_type == CartItemType.instamart:
        if item_id not in INSTAMART_ITEMS:
            raise ValueError(f"Unknown mock item: {item_id}")
        return INSTAMART_ITEMS[item_id]

    raise ValueError(f"Unsupported item_type: {item_type}")


def _to_terms(query: str) -> list[str]:
    return [term for term in query.lower().replace(",", " ").split() if len(term) > 1]


def _matches_terms(name: str, terms: list[str]) -> bool:
    lowered = name.lower()
    return any(term in lowered for term in terms)


def _get_cart(cart_id: str) -> Cart:
    if cart_id not in CARTS:
        raise ValueError(f"Unknown cart: {cart_id}")
    return CARTS[cart_id]


def _recalculate(cart: Cart) -> Cart:
    cart.subtotal = sum(item.line_total for item in cart.items)
    cart.item_count = sum(item.quantity for item in cart.items)
    cart.delivery_fee = 39 if cart.items else 0
    cart.discount = min(50, cart.subtotal // 10) if cart.applied_coupon else 0
    cart.total = max(cart.subtotal + cart.delivery_fee - cart.discount, 0)
    CARTS[cart.cart_id] = cart
    return cart
