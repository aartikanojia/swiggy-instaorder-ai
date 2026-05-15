from app.adapters import mock_swiggy_tools
from app.models.cart import Cart, CartItem, MockOrder, Workflow


class SwiggyMcpAdapter:
    """Adapter boundary for mock tools now and real Swiggy MCP later."""

    def search_food(self, query: str, budget: int | None = None) -> list[CartItem]:
        return mock_swiggy_tools.search_food(query, budget)

    def search_instamart_items(self, query: str, budget: int | None = None) -> list[CartItem]:
        return mock_swiggy_tools.search_instamart_items(query, budget)

    def create_cart(self, workflow: Workflow) -> Cart:
        return mock_swiggy_tools.create_cart(workflow)

    def add_item_to_cart(self, cart_id: str, item_id: str, quantity: int = 1) -> Cart:
        return mock_swiggy_tools.add_item_to_cart(cart_id, item_id, quantity)

    def remove_item_from_cart(self, cart_id: str, item_id: str, quantity: int | None = None) -> Cart:
        return mock_swiggy_tools.remove_item_from_cart(cart_id, item_id, quantity)

    def review_cart(self, cart_id: str) -> Cart:
        return mock_swiggy_tools.review_cart(cart_id)

    def apply_coupon_mock(self, cart_id: str, coupon_code: str) -> Cart:
        return mock_swiggy_tools.apply_coupon_mock(cart_id, coupon_code)

    def confirm_checkout_mock(self, cart_id: str) -> MockOrder:
        return mock_swiggy_tools.confirm_checkout_mock(cart_id)

    def track_order_mock(self, order_id: str | None = None) -> MockOrder:
        return mock_swiggy_tools.track_order_mock(order_id)
