from app.adapters.swiggy_mcp_adapter import SwiggyMcpAdapter
from app.models.cart import Cart, CartItemType, Workflow
from app.services.intent_service import IntentName, ParsedIntent


class CartService:
    def __init__(self, adapter: SwiggyMcpAdapter | None = None) -> None:
        self.adapter = adapter or SwiggyMcpAdapter()

    def create_cart(self, user_id: str, workflow: Workflow | None = None) -> Cart:
        return self.adapter.create_cart(user_id=user_id, workflow=workflow)

    def add_item_to_cart(self, cart_id: str, item_id: str, item_type: CartItemType, quantity: int = 1) -> Cart:
        return self.adapter.add_item_to_cart(cart_id, item_id, item_type, quantity)

    def remove_item_from_cart(self, cart_id: str, item_id: str) -> Cart:
        return self.adapter.remove_item_from_cart(cart_id, item_id)

    def update_item_quantity(self, cart_id: str, item_id: str, quantity: int) -> Cart:
        return self.adapter.update_item_quantity(cart_id, item_id, quantity)

    def review_cart(self, cart_id: str) -> Cart:
        return self.adapter.review_cart(cart_id)

    def clear_cart(self, cart_id: str) -> Cart:
        return self.adapter.clear_cart(cart_id)

    def apply_coupon(self, cart_id: str, coupon_code: str) -> Cart:
        return self.adapter.apply_coupon_mock(cart_id, coupon_code)

    def prepare_cart_from_intent(self, intent: ParsedIntent) -> Cart:
        workflow = intent.workflow or Workflow.food
        item_type = CartItemType.instamart if intent.intent == IntentName.instamart_search else CartItemType.food
        cart = self.create_cart(user_id="assistant-user", workflow=workflow)

        if intent.intent == IntentName.instamart_search:
            items = self.adapter.search_instamart_items(query=intent.query, max_price=intent.budget)
        else:
            items = self.adapter.search_food(query=intent.query, budget=intent.budget)

        for item in items[:3]:
            self.add_item_to_cart(cart.cart_id, item["id"], item_type, 1)
        return self.review_cart(cart.cart_id)
