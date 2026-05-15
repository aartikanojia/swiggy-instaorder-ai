from enum import StrEnum

from pydantic import BaseModel, Field


class Workflow(StrEnum):
    food = "food"
    instamart = "instamart"


class CartStatus(StrEnum):
    draft = "draft"
    reviewed = "reviewed"
    checked_out = "checked_out"


class CartItem(BaseModel):
    item_id: str
    name: str
    quantity: int = Field(ge=1)
    unit_price: int = Field(ge=0)
    source: str = "mock"
    available: bool = True

    @property
    def line_total(self) -> int:
        return self.unit_price * self.quantity


class Cart(BaseModel):
    cart_id: str
    workflow: Workflow
    status: CartStatus = CartStatus.draft
    items: list[CartItem] = Field(default_factory=list)
    subtotal: int = 0
    discount: int = 0
    delivery_fee: int = 0
    total: int = 0
    currency: str = "INR"
    mock: bool = True
    applied_coupon: str | None = None


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
