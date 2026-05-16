from pydantic import BaseModel, Field

from app.models.cart import CartItemType, Workflow


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    last_order_id: str | None = None


class CreateCartRequest(BaseModel):
    user_id: str = Field(min_length=1)


class AddCartItemRequest(BaseModel):
    item_id: str = Field(min_length=1)
    item_type: CartItemType
    quantity: int = Field(default=1, ge=1, le=20)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(ge=1, le=20)


class AddItemRequest(BaseModel):
    item_id: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1, le=20)


class RemoveItemRequest(BaseModel):
    quantity: int | None = Field(default=None, ge=1, le=20)


class CreateLegacyCartRequest(BaseModel):
    workflow: Workflow


class ApplyCouponRequest(BaseModel):
    coupon_code: str = Field(min_length=1, max_length=32)


class CheckoutRequest(BaseModel):
    cart_id: str = Field(min_length=1)
    user_confirmation: bool = False
