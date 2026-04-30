# Architecture

Swiggy InstaOrder AI uses a backend-first architecture. The client and AI assistant provide the user experience, while business rules, cart state, policy enforcement, and tool execution are handled by backend services.

The project is mock-first. Initial development uses mock Swiggy tools so the ordering flow, safety checks, and service boundaries can be validated before any real Swiggy MCP integration is added.

## High-Level Flow

```text
User
  -> Client / AI Assistant
  -> FastAPI Backend
  -> Intent Service
  -> Policy Service
  -> Cart / Order Service
  -> Swiggy MCP Adapter
  -> Mock Swiggy Tools initially
  -> Real Swiggy MCP after approval
```

## Components

### Client / AI Assistant

The client captures user requests and presents search results, cart summaries, order status, and confirmation prompts. It does not own business logic or checkout rules.

### FastAPI Backend

The backend exposes API routes for assistant, cart, order, and health workflows. Routes should remain thin and delegate behavior to services.

### Intent Service

The intent service interprets user requests, classifies food or grocery workflows, and extracts structured parameters such as budget, dietary preferences, item names, or order-tracking intent.

### Policy Service

The policy service enforces safety requirements before tool execution. It verifies explicit confirmation, blocks real checkout when access is not approved, and prevents unsafe or unsupported behavior.

### Cart Service

The cart service manages mock cart creation, item changes, review summaries, and order state. It should keep cart behavior deterministic and auditable.

### Swiggy MCP Adapter

The adapter is the boundary between backend services and tool execution. During the mock phase, it calls local mock tools. After approval, it can route supported calls to real Swiggy MCP endpoints.

## Planned Real MCP Endpoints

- `https://mcp.swiggy.com/food`
- `https://mcp.swiggy.com/im`

## Mandatory Checkout Sequence

1. User asks for order/cart.
2. Assistant prepares cart.
3. Backend validates cart.
4. User reviews cart.
5. User explicitly confirms.
6. Backend executes checkout.

## Deployment Direction

Future deployment may use Azure Container Apps with an HTTPS endpoint, managed secrets, environment-based configuration, and basic monitoring/logs.
