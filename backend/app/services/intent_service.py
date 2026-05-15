from enum import StrEnum

from pydantic import BaseModel, Field

from app.models.cart import Workflow


class IntentName(StrEnum):
    food_search = "food_search"
    instamart_search = "instamart_search"
    track_order = "track_order"


class ParsedIntent(BaseModel):
    intent: IntentName
    workflow: Workflow | None = None
    query: str = Field(default="")
    budget: int | None = None


class IntentService:
    def parse(self, message: str) -> ParsedIntent:
        normalized = message.strip().lower()
        budget = self._extract_budget(normalized)

        if "track" in normalized or "last order" in normalized:
            return ParsedIntent(intent=IntentName.track_order, query=message)

        grocery_terms = ["instamart", "milk", "eggs", "bread", "fruits", "grocery", "groceries"]
        if any(term in normalized for term in grocery_terms):
            return ParsedIntent(
                intent=IntentName.instamart_search,
                workflow=Workflow.instamart,
                query=message,
                budget=budget,
            )

        return ParsedIntent(
            intent=IntentName.food_search,
            workflow=Workflow.food,
            query=message,
            budget=budget,
        )

    def _extract_budget(self, normalized: str) -> int | None:
        tokens = normalized.replace("₹", " ").replace(",", " ").split()
        for token in tokens:
            if token.isdigit():
                return int(token)
        return None
