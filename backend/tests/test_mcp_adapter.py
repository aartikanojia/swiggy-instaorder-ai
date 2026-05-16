from app.adapters.swiggy_mcp_adapter import SwiggyMcpAdapter
from app.adapters.swiggy_mcp_client import AccessPendingError, MockSwiggyMcpClient
from app.core.config import get_settings


class StubClient:
    def __init__(self) -> None:
        self.food_calls = []
        self.instamart_calls = []

    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[dict]:
        self.food_calls.append(
            {"query": query, "budget": budget, "cuisine": cuisine, "veg_only": veg_only}
        )
        return [{"id": "food-stub", "name": "Stub Food", "cuisine": "Test", "price": 100, "availability": True, "source": "mock"}]

    def search_instamart_items(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        self.instamart_calls.append(
            {"query": query, "category": category, "max_price": max_price}
        )
        return [{"id": "im-stub", "name": "Stub Item", "category": "Test", "price": 50, "availability": True, "source": "mock"}]


def test_adapter_defaults_to_mock_client() -> None:
    get_settings.cache_clear()
    adapter = SwiggyMcpAdapter()
    assert isinstance(adapter.client, MockSwiggyMcpClient)


def test_food_search_flows_through_adapter_client() -> None:
    stub_client = StubClient()
    adapter = SwiggyMcpAdapter(client=stub_client)

    result = adapter.search_food(query="paneer", budget=300, cuisine="North Indian", veg_only=True)

    assert result[0]["id"] == "food-stub"
    assert stub_client.food_calls == [{"query": "paneer", "budget": 300, "cuisine": "North Indian", "veg_only": True}]


def test_instamart_search_flows_through_adapter_client() -> None:
    stub_client = StubClient()
    adapter = SwiggyMcpAdapter(client=stub_client)

    result = adapter.search_instamart_items(query="milk", category="Dairy", max_price=90)

    assert result[0]["id"] == "im-stub"
    assert stub_client.instamart_calls == [{"query": "milk", "category": "Dairy", "max_price": 90}]


def test_real_mode_fails_safely(monkeypatch) -> None:
    monkeypatch.setenv("INSTAORDER_MODE", "real")
    get_settings.cache_clear()
    adapter = SwiggyMcpAdapter()

    try:
        adapter.search_food(query="bowl")
        raise AssertionError("Expected AccessPendingError in real mode.")
    except AccessPendingError as exc:
        assert "not enabled" in str(exc)
    finally:
        monkeypatch.delenv("INSTAORDER_MODE", raising=False)
        get_settings.cache_clear()
