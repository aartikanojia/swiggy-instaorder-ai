from typing import Protocol

from app.adapters import mock_swiggy_tools


class AccessPendingError(NotImplementedError):
    """Raised when real Swiggy MCP integration is requested before approval."""


class SwiggyMcpClient(Protocol):
    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[dict]:
        ...

    def search_instamart_items(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        ...


class MockSwiggyMcpClient:
    """Default mock-first client that proxies to local mock tools."""

    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[dict]:
        return mock_swiggy_tools.search_food(query=query, budget=budget, cuisine=cuisine, veg_only=veg_only)

    def search_instamart_items(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        return mock_swiggy_tools.search_instamart_items(query=query, category=category, max_price=max_price)


class RealSwiggyMcpClient:
    """Placeholder for real Swiggy MCP streamable HTTP integration."""

    def __init__(
        self,
        food_endpoint: str = "https://mcp.swiggy.com/food",
        instamart_endpoint: str = "https://mcp.swiggy.com/im",
        dineout_endpoint: str = "https://mcp.swiggy.com/dineout",
    ) -> None:
        self.food_endpoint = food_endpoint
        self.instamart_endpoint = instamart_endpoint
        self.dineout_endpoint = dineout_endpoint

    def search_food(
        self,
        query: str = "",
        budget: int | None = None,
        cuisine: str | None = None,
        veg_only: bool = False,
    ) -> list[dict]:
        raise AccessPendingError(
            "Real Swiggy MCP food integration is not enabled. Access approval and auth implementation are pending."
        )

    def search_instamart_items(
        self,
        query: str = "",
        category: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        raise AccessPendingError(
            "Real Swiggy MCP Instamart integration is not enabled. Access approval and auth implementation are pending."
        )
