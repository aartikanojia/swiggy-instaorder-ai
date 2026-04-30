# Roadmap

## Phase 0 — Documentation and Access Application

Goal: Define the project, safety boundaries, and implementation plan for Swiggy Builders Kitchen review.

Tasks:

- Create repository documentation.
- Define architecture and safety rules.
- Document mock-first development approach.
- Prepare for official Swiggy MCP access application.

## Phase 1 — Mock Backend

Goal: Build a backend-first prototype using mock tools only.

Tasks:

- Create FastAPI project structure.
- Add health, assistant, cart, and order routes.
- Implement mock food and Instamart search tools.
- Implement mock cart and mock order state.
- Add focused tests for policy and cart behavior.

## Phase 2 — Agent Flow

Goal: Connect natural language requests to structured backend actions.

Tasks:

- Add intent parsing for food, grocery, cart, checkout, and tracking requests.
- Prepare cart suggestions from mock search results.
- Add review-before-confirmation flow.
- Require explicit confirmation before checkout.
- Keep prompts advisory and enforce rules in backend services.

## Phase 3 — MCP Adapter Boundary

Goal: Create a clean boundary between backend services and tool execution.

Tasks:

- Define adapter interfaces for food search, Instamart search, cart, checkout, and tracking.
- Route mock tool execution through the adapter layer.
- Keep API routes independent from mock or real MCP implementation details.
- Add tests that verify checkout cannot bypass policy checks.

## Phase 4 — Real Swiggy MCP Integration

Goal: Replace mock adapter behavior with approved Swiggy MCP calls.

Status: Blocked until Swiggy access approval.

Tasks:

- Configure approved Swiggy MCP credentials through environment variables or managed secrets.
- Integrate Swiggy Food MCP.
- Integrate Swiggy Instamart MCP.
- Source price, availability, delivery estimates, discounts, and offers from Swiggy MCP responses.
- Validate attribution, access-control, and checkout requirements.

## Phase 5 — Frontend

Goal: Provide a user interface for discovery, cart review, confirmation, and tracking.

Tasks:

- Choose a frontend option.
- Build UI-only client screens.
- Connect client to backend APIs.
- Show clear cart review and confirmation states.
- Keep checkout controls tied to backend policy checks.

Possible frontend options:

- Simple web UI.
- Flutter mobile UI.
- CLI assistant for local use.

## Phase 6 — Deployment

Goal: Deploy a secure prototype with environment-based configuration.

Tasks:

- Package backend for deployment.
- Deploy to Azure Container Apps as a possible option.
- Expose an HTTPS endpoint.
- Use managed secrets for credentials.
- Configure environment-based settings.
- Add basic monitoring and logs.
