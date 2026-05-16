from fastapi import APIRouter, Query

from app.models.responses import InstamartSearchResult
from app.services.search_service import SearchService

router = APIRouter(prefix="/instamart", tags=["instamart"])
search_service = SearchService()


@router.get("/search", response_model=list[InstamartSearchResult])
def search_instamart(
    query: str = "",
    category: str | None = None,
    max_price: int | None = Query(default=None, ge=0),
) -> list[InstamartSearchResult]:
    return search_service.search_instamart(query=query, category=category, max_price=max_price)
