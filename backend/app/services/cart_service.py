from app.adapters.swiggy_mcp_adapter import SwiggyMcpAdapter
from app.models.cart import Cart, Workflow
from app.services.intent_service import IntentName, ParsedIntent


class CartService:
    def __init__(self, adapter: SwiggyMcpAdapter | None = None) -> None:
        self.adapter = adapter or SwiggyMcpAdapter()

    def create_cart(self, workflow: Workflow) -> Cart:
        return self.adapter.create_cart(workflow)

    def add_item(self, cart_id: str, item_id: str, quantity: int = 1) -> Cart:
        return self.adapter.add_item_to_cart(cart_id, item_id, quantity)

    def remove_item(self, cart_id: str, item_id: str, quantity: int | None = None) -> Cart:
        return self.adapter.remove_item_from_cart(cart_id, item_id, quantity)

    def review_cart(self, cart_id: str) -> Cart:
        return self.adapter.review_cart(cart_id)

    def apply_coupon(self, cart_id: str, coupon_code: str) -> Cart:
        return self.adapter.apply_coupon_mock(cart_id, coupon_code)

    def prepare_cart_from_intent(self, intent: ParsedIntent) -> Cart:
        workflow = intent.workflow or Workflow.food
        cart = self.create_cart(workflow)

        if intent.intent == IntentName.instamart_search:
            items = self.adapter.search_instamart_items(query=intent.query, max_price=intent.budget)
        else:
            items = self.adapter.search_food(query=intent.query, budget=intent.budget)

        for item in items[:3]:
            cart = self.add_item(cart.cart_id, item["id"], 1)
        return self.review_cart(cart.cart_id)
