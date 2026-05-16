from pydantic import BaseModel

from app.models.cart import Cart, MockOrder
from app.services.intent_service import ParsedIntent


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    mode: str


class AssistantResponse(BaseModel):
    message: str
    intent: ParsedIntent
    cart: Cart | None = None
    order: MockOrder | None = None
    requires_confirmation: bool


class CheckoutResponse(BaseModel):
    message: str
    order: MockOrder


class OrderResponse(MockOrder):
    pass


class FoodSearchResult(BaseModel):
    id: str
    name: str
    cuisine: str
    price: int
    availability: bool
    source: str = "mock"


class InstamartSearchResult(BaseModel):
    id: str
    name: str
    category: str
    price: int
    availability: bool
    source: str = "mock"
