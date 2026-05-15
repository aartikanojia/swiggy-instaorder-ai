from fastapi import APIRouter

from app.models.requests import AssistantRequest
from app.models.responses import AssistantResponse
from app.services.cart_service import CartService
from app.services.intent_service import IntentService
from app.services.order_service import OrderService

router = APIRouter(prefix="/assistant", tags=["assistant"])

intent_service = IntentService()
cart_service = CartService()
order_service = OrderService()


@router.post("/message", response_model=AssistantResponse)
def handle_message(request: AssistantRequest) -> AssistantResponse:
    intent = intent_service.parse(request.message)

    if intent.intent == "track_order":
        order = order_service.track_order(request.last_order_id)
        return AssistantResponse(
            message=f"Mock tracking status: {order.status}.",
            intent=intent,
            order=order,
            requires_confirmation=False,
        )

    cart = cart_service.prepare_cart_from_intent(intent)
    return AssistantResponse(
        message="I prepared a mock cart for review. Checkout requires explicit confirmation.",
        intent=intent,
        cart=cart,
        requires_confirmation=True,
    )
