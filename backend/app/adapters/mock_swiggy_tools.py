from itertools import count

from app.models.cart import Cart, CartItem, CartStatus, MockOrder, OrderStatus, Workflow

_cart_counter = count(1)
_order_counter = count(1)

FOOD_ITEMS = {
    "food-paneer-bowl": CartItem(item_id="food-paneer-bowl", name="Paneer protein bowl", quantity=1, unit_price=249),
    "food-snack-combo": CartItem(item_id="food-snack-combo", name="Evening snacks combo", quantity=1, unit_price=199),
    "food-healthy-thali": CartItem(item_id="food-healthy-thali", name="Healthy dinner thali", quantity=1, unit_price=289),
    "food-sprout-chaat": CartItem(item_id="food-sprout-chaat", name="High-protein sprout chaat", quantity=1, unit_price=149),
}

INSTAMART_ITEMS = {
    "im-milk": CartItem(item_id="im-milk", name="Milk 1L", quantity=1, unit_price=68),
    "im-eggs": CartItem(item_id="im-eggs", name="Eggs pack of 6", quantity=1, unit_price=84),
    "im-bread": CartItem(item_id="im-bread", name="Whole wheat bread", quantity=1, unit_price=55),
    "im-fruits": CartItem(item_id="im-fruits", name="Seasonal fruit pack", quantity=1, unit_price=179),
    "im-protein-snack": CartItem(item_id="im-protein-snack", name="Roasted chana snack", quantity=1, unit_price=65),
}

CARTS: dict[str, Cart] = {}
ORDERS: dict[str, MockOrder] = {}


def search_food(query: str, budget: int | None = None) -> list[CartItem]:
    return _filter_items(list(FOOD_ITEMS.values()), query, budget)


def search_instamart_items(query: str, budget: int | None = None) -> list[CartItem]:
    return _filter_items(list(INSTAMART_ITEMS.values()), query, budget)


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


def _filter_items(items: list[CartItem], query: str, budget: int | None) -> list[CartItem]:
    terms = [term for term in query.lower().replace(",", " ").split() if len(term) > 2]
    results = [
        item for item in items if not budget or item.unit_price <= budget
    ]
    matched = [
        item for item in results if any(term in item.name.lower() for term in terms)
    ]
    return matched or results[:3]


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
