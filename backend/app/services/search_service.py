from app.adapters.swiggy_mcp_adapter import SwiggyMcpAdapter
from app.models.responses import FoodSearchResult, InstamartSearchResult


class SearchService:
    def __init__(self, adapter: SwiggyMcpAdapter | None = None) -> None:
        self.adapter = adapter or SwiggyMcpAdapter()

    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[FoodSearchResult]:
        results = self.adapter.search_food(query=query, budget=budget, cuisine=cuisine, veg_only=veg_only)
        return [FoodSearchResult(**item) for item in results]

    def search_instamart(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[InstamartSearchResult]:
        results = self.adapter.search_instamart_items(query=query, category=category, max_price=max_price)
        return [InstamartSearchResult(**item) for item in results]
