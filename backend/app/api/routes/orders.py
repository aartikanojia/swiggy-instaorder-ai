from fastapi import APIRouter, HTTPException, status

from app.models.requests import CheckoutRequest
from app.models.responses import CheckoutResponse, OrderResponse
from app.services.order_service import OrderService
from app.services.policy_service import PolicyError

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService()


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(request: CheckoutRequest) -> CheckoutResponse:
    try:
        return order_service.checkout(request.cart_id, request.user_confirmation)
    except PolicyError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{order_id}", response_model=OrderResponse)
def track_order(order_id: str) -> OrderResponse:
    try:
        return order_service.track_order(order_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
