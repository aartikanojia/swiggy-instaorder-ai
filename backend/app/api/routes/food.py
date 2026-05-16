from fastapi import APIRouter, Query

from app.models.responses import FoodSearchResult
from app.services.search_service import SearchService

router = APIRouter(prefix="/food", tags=["food"])
search_service = SearchService()


@router.get("/search", response_model=list[FoodSearchResult])
def search_food(
    query: str = "",
    budget: int | None = Query(default=None, ge=0),
    cuisine: str | None = None,
    veg_only: bool = False,
) -> list[FoodSearchResult]:
    return search_service.search_food(query=query, budget=budget, cuisine=cuisine, veg_only=veg_only)
