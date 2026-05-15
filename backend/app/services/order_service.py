from app.adapters.swiggy_mcp_adapter import SwiggyMcpAdapter
from app.models.responses import CheckoutResponse, OrderResponse
from app.services.policy_service import PolicyService


class OrderService:
    def __init__(
        self,
        adapter: SwiggyMcpAdapter | None = None,
        policy_service: PolicyService | None = None,
    ) -> None:
        self.adapter = adapter or SwiggyMcpAdapter()
        self.policy_service = policy_service or PolicyService()

    def checkout(self, cart_id: str, user_confirmation: bool) -> CheckoutResponse:
        cart = self.adapter.review_cart(cart_id)
        self.policy_service.validate_checkout(cart, user_confirmation)
        order = self.adapter.confirm_checkout_mock(cart.cart_id)
        return CheckoutResponse(message="Mock checkout confirmed.", order=order)

    def track_order(self, order_id: str | None = None) -> OrderResponse:
        order = self.adapter.track_order_mock(order_id)
        return OrderResponse(**order.model_dump())
