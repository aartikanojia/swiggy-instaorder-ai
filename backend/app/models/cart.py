from enum import StrEnum

from pydantic import BaseModel, Field


class Workflow(StrEnum):
    food = "food"
    instamart = "instamart"


class CartItemType(StrEnum):
    food = "food"
    instamart = "instamart"


class CartStatus(StrEnum):
    draft = "draft"
    reviewed = "reviewed"
    checked_out = "checked_out"


class CartItem(BaseModel):
    item_id: str
    name: str
    item_type: CartItemType
    price: int = Field(ge=0)
    quantity: int = Field(ge=1)
    availability: bool = True

    @property
    def line_total(self) -> int:
        return self.price * self.quantity


class Cart(BaseModel):
    cart_id: str
    user_id: str
    items: list[CartItem] = Field(default_factory=list)
    subtotal: int = 0
    item_count: int = 0
    source: str = "mock"
    status: CartStatus = CartStatus.draft

    # Backward-compatible fields retained for existing flows.
    discount: int = 0
    delivery_fee: int = 0
    total: int = 0
    currency: str = "INR"
    applied_coupon: str | None = None
    workflow: Workflow | None = None

    @property
    def mock(self) -> bool:
        return self.source == "mock"


class CartReview(BaseModel):
    cart_id: str
    user_id: str
    items: list[CartItem]
    subtotal: int
    item_count: int
    source: str = "mock"


class OrderStatus(StrEnum):
    placed = "placed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class MockOrder(BaseModel):
    order_id: str
    cart_id: str
    status: OrderStatus = OrderStatus.placed
    eta_minutes: int = 35
    mock: bool = True
