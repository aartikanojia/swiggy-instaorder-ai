import json
from itertools import count
from pathlib import Path

from app.models.cart import Cart, CartItem, CartStatus, MockOrder, OrderStatus, Workflow

_cart_counter = count(1)
_order_counter = count(1)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FOOD_DATA: list[dict] = json.loads((DATA_DIR / "mock_food.json").read_text(encoding="utf-8"))
INSTAMART_DATA: list[dict] = json.loads((DATA_DIR / "mock_instamart.json").read_text(encoding="utf-8"))

FOOD_ITEMS = {
    item["id"]: CartItem(item_id=item["id"], name=item["name"], quantity=1, unit_price=item["price"])
    for item in FOOD_DATA
}
INSTAMART_ITEMS = {
    item["id"]: CartItem(item_id=item["id"], name=item["name"], quantity=1, unit_price=item["price"])
    for item in INSTAMART_DATA
}

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


def create_cart(workflow: Workflow) -> Cart:
    cart = Cart(cart_id=f"mock-cart-{next(_cart_counter)}", workflow=workflow)
    CARTS[cart.cart_id] = cart
    return cart


def add_item_to_cart(cart_id: str, item_id: str, quantity: int = 1) -> Cart:
    cart = _get_cart(cart_id)
    catalog = FOOD_ITEMS if cart.workflow == Workflow.food else INSTAMART_ITEMS
    if item_id not in catalog:
        raise ValueError(f"Unknown mock item: {item_id}")

    item = catalog[item_id].model_copy(update={"quantity": quantity})
    existing = next((cart_item for cart_item in cart.items if cart_item.item_id == item_id), None)
    if existing:
        existing.quantity += quantity
    else:
        cart.items.append(item)
    return _recalculate(cart)


def remove_item_from_cart(cart_id: str, item_id: str, quantity: int | None = None) -> Cart:
    cart = _get_cart(cart_id)
    existing = next((cart_item for cart_item in cart.items if cart_item.item_id == item_id), None)
    if not existing:
        raise ValueError(f"Item is not in cart: {item_id}")

    if quantity is None or quantity >= existing.quantity:
        cart.items = [cart_item for cart_item in cart.items if cart_item.item_id != item_id]
    else:
        existing.quantity -= quantity
    return _recalculate(cart)


def review_cart(cart_id: str) -> Cart:
    cart = _get_cart(cart_id)
    cart.status = CartStatus.reviewed
    return _recalculate(cart)


def apply_coupon_mock(cart_id: str, coupon_code: str) -> Cart:
    cart = _get_cart(cart_id)
    cart.applied_coupon = coupon_code.upper()
    return _recalculate(cart)


def confirm_checkout_mock(cart_id: str) -> MockOrder:
    cart = review_cart(cart_id)
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
    cart.delivery_fee = 39 if cart.items else 0
    cart.discount = min(50, cart.subtotal // 10) if cart.applied_coupon else 0
    cart.total = max(cart.subtotal + cart.delivery_fee - cart.discount, 0)
    CARTS[cart.cart_id] = cart
    return cart
