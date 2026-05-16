# Swiggy InstaOrder AI

Swiggy InstaOrder AI is a mock-first personal AI ordering assistant prototype for Swiggy Food MCP and Swiggy Instamart MCP workflows.

The assistant is designed to help users discover food and grocery options, prepare carts, review items, and complete checkout only after explicit user confirmation. Real Swiggy MCP calls will be added only after official access is approved.

## Example Requests

- "Order my usual evening snacks."
- "Find healthy dinner options under ₹300."
- "Add milk, eggs, bread, and fruits to my Instamart cart."
- "Show me high-protein snacks available nearby."
- "Track my last order."

## Planned MCP Integration

After official access approval, the backend will integrate with:

- Swiggy Food MCP
- Swiggy Instamart MCP

Until then, all search, cart, checkout, and order tracking behavior will use mock tools and mock data.

## High-Level Architecture

```text
Client / AI Assistant
  -> FastAPI Backend
  -> Intent + Policy + Cart Orchestration
  -> Swiggy MCP Adapter
  -> Swiggy Food MCP / Swiggy Instamart MCP
```

## Safety Rule

```text
AI can recommend.
Backend validates.
User confirms.
Tool executes.
```

The assistant may suggest items and carts, but backend policy checks must enforce confirmation, privacy, and integration rules before any tool execution.

## Non-Goals

- No scraping.
- No reverse engineering Swiggy APIs.
- No bypassing Swiggy MCP access control.
- No misrepresenting prices, availability, or delivery time.
- No checkout without explicit user confirmation.
- No payment/card data storage.

## Current Status

This repository includes a mock-first FastAPI backend with:

- Mock Food and Instamart search
- Mock cart lifecycle (create, add, update quantity, remove, review, clear)
- Mock checkout and mock order tracking guarded by policy checks
- Swiggy MCP adapter/client boundary with real client placeholder disabled

Real Swiggy MCP calls remain disabled until official access is approved.

## Cart API (Mock)

- `POST /api/v1/cart` (create cart with `user_id`)
- `POST /api/v1/cart/{cart_id}/items` (add item with `item_id`, `item_type`, `quantity`)
- `PATCH /api/v1/cart/{cart_id}/items/{item_id}` (update item quantity)
- `DELETE /api/v1/cart/{cart_id}/items/{item_id}` (remove item)
- `GET /api/v1/cart/{cart_id}` (review cart)
- `DELETE /api/v1/cart/{cart_id}/items` (clear cart)

## Backend Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn app.main:app --app-dir backend --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Run tests:

```bash
python -m pytest
```

## Planned Phases

1. Documentation and access application. Complete.
2. Mock FastAPI backend with mock food and Instamart tools. Complete.
3. Agent flow for intent parsing, cart preparation, review, and confirmation. In progress.
4. MCP adapter boundary for swapping mock tools with real Swiggy MCP calls. Complete.
5. Real Swiggy MCP integration after access approval.
6. UI and deployment.

## Documentation

- [Architecture](docs/architecture.md)
- [Security and Privacy](docs/security-and-privacy.md)
- [Roadmap](docs/roadmap.md)
