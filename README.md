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

This repository is in the documentation and access-application phase. It defines the intended architecture, safety boundaries, and implementation roadmap for a backend-first prototype.

## Planned Phases

1. Documentation and access application.
2. Mock FastAPI backend with mock food and Instamart tools.
3. Agent flow for intent parsing, cart preparation, review, and confirmation.
4. MCP adapter boundary for swapping mock tools with real Swiggy MCP calls.
5. Real Swiggy MCP integration after access approval.
6. UI and deployment.

## Documentation

- [Architecture](docs/architecture.md)
- [Security and Privacy](docs/security-and-privacy.md)
- [Roadmap](docs/roadmap.md)
