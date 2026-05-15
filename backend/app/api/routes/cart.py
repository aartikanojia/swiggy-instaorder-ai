from fastapi import APIRouter, HTTPException, status

from app.models.cart import Cart
from app.models.requests import AddItemRequest, ApplyCouponRequest, CreateCartRequest, RemoveItemRequest
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])
cart_service = CartService()


@router.post("", response_model=Cart, status_code=status.HTTP_201_CREATED)
def create_cart(request: CreateCartRequest) -> Cart:
    return cart_service.create_cart(request.workflow)


@router.post("/{cart_id}/items", response_model=Cart)
def add_item(cart_id: str, request: AddItemRequest) -> Cart:
    try:
        return cart_service.add_item(cart_id, request.item_id, request.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{cart_id}/items/{item_id}", response_model=Cart)
def remove_item(cart_id: str, item_id: str, request: RemoveItemRequest | None = None) -> Cart:
    quantity = request.quantity if request else None
    try:
        return cart_service.remove_item(cart_id, item_id, quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{cart_id}/review", response_model=Cart)
def review_cart(cart_id: str) -> Cart:
    try:
        return cart_service.review_cart(cart_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{cart_id}/coupon", response_model=Cart)
def apply_coupon(cart_id: str, request: ApplyCouponRequest) -> Cart:
    try:
        return cart_service.apply_coupon(cart_id, request.coupon_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
