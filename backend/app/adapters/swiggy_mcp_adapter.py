from app.adapters import mock_swiggy_tools
from app.adapters.swiggy_mcp_client import MockSwiggyMcpClient, RealSwiggyMcpClient, SwiggyMcpClient
from app.core.config import get_settings
from app.models.cart import Cart, CartItemType, MockOrder, Workflow


class SwiggyMcpAdapter:
    """Adapter boundary for mock tools now and real Swiggy MCP later."""

    def __init__(self, client: SwiggyMcpClient | None = None) -> None:
        self.client = client or self._default_client()

    def _default_client(self) -> SwiggyMcpClient:
        settings = get_settings()
        if settings.mode == "real":
            return RealSwiggyMcpClient(
                food_endpoint=settings.swiggy_food_mcp_url,
                instamart_endpoint=settings.swiggy_instamart_mcp_url,
            )
        return MockSwiggyMcpClient()

    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[dict]:
        return self.client.search_food(query=query, budget=budget, cuisine=cuisine, veg_only=veg_only)

    def search_instamart_items(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        return self.client.search_instamart_items(query=query, category=category, max_price=max_price)

    def create_cart(self, user_id: str, workflow: Workflow | None = None) -> Cart:
        return mock_swiggy_tools.create_cart(user_id=user_id, workflow=workflow)

    def add_item_to_cart(self, cart_id: str, item_id: str, item_type: CartItemType, quantity: int = 1) -> Cart:
        return mock_swiggy_tools.add_item_to_cart(cart_id, item_id, item_type, quantity)

    def remove_item_from_cart(self, cart_id: str, item_id: str) -> Cart:
        return mock_swiggy_tools.remove_item_from_cart(cart_id, item_id)

    def update_item_quantity(self, cart_id: str, item_id: str, quantity: int) -> Cart:
        return mock_swiggy_tools.update_item_quantity(cart_id, item_id, quantity)

    def review_cart(self, cart_id: str) -> Cart:
        return mock_swiggy_tools.review_cart(cart_id)

    def clear_cart(self, cart_id: str) -> Cart:
        return mock_swiggy_tools.clear_cart(cart_id)

    def apply_coupon_mock(self, cart_id: str, coupon_code: str) -> Cart:
        return mock_swiggy_tools.apply_coupon_mock(cart_id, coupon_code)

    def confirm_checkout_mock(self, cart_id: str) -> MockOrder:
        return mock_swiggy_tools.confirm_checkout_mock(cart_id)

    def track_order_mock(self, order_id: str | None = None) -> MockOrder:
        return mock_swiggy_tools.track_order_mock(order_id)
