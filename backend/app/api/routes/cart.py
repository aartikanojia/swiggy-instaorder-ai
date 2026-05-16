from fastapi import APIRouter, HTTPException, status

from app.models.cart import Cart, CartReview
from app.models.requests import AddCartItemRequest, CreateCartRequest, UpdateCartItemRequest
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])
cart_service = CartService()


@router.post("", response_model=Cart, status_code=status.HTTP_201_CREATED)
def create_cart(request: CreateCartRequest) -> Cart:
    return cart_service.create_cart(user_id=request.user_id)


@router.post("/{cart_id}/items", response_model=Cart)
def add_item(cart_id: str, request: AddCartItemRequest) -> Cart:
    try:
        return cart_service.add_item_to_cart(cart_id, request.item_id, request.item_type, request.quantity)
    except ValueError as exc:
        error_status = status.HTTP_404_NOT_FOUND if "Unknown" in str(exc) or "not in cart" in str(exc) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=error_status, detail=str(exc)) from exc


@router.patch("/{cart_id}/items/{item_id}", response_model=Cart)
def update_item_quantity(cart_id: str, item_id: str, request: UpdateCartItemRequest) -> Cart:
    try:
        return cart_service.update_item_quantity(cart_id, item_id, request.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{cart_id}/items/{item_id}", response_model=Cart)
def remove_item(cart_id: str, item_id: str) -> Cart:
    try:
        return cart_service.remove_item_from_cart(cart_id, item_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{cart_id}", response_model=CartReview)
def review_cart(cart_id: str) -> CartReview:
    try:
        return cart_service.review_cart(cart_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{cart_id}/items", response_model=Cart)
def clear_cart(cart_id: str) -> Cart:
    try:
        return cart_service.clear_cart(cart_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
