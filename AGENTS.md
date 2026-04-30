# AGENTS.md

## Project

Swiggy InstaOrder AI is a backend-first, mock-first AI ordering assistant prototype for Swiggy Food MCP and Swiggy Instamart MCP workflows.

Coding agents working in this repository should keep the implementation professional, safety-focused, and suitable for sharing in the Swiggy Builders Kitchen developer application.

## Agent Role

Codex and other coding agents should help build a personal ordering assistant that can:

- Understand user food and grocery intents.
- Search mock food and Instamart options.
- Prepare and review carts.
- Track mock order state.
- Execute checkout only after explicit user confirmation.

Do not create real Swiggy integrations until official Swiggy MCP access is approved.

## Architecture Rules

- Frontend is UI-only.
- Business logic stays in backend services.
- API routes only route/orchestrate.
- Tool execution goes through a service/MCP adapter layer.
- Do not put checkout or payment logic inside LLM prompts.
- Keep credentials in environment variables.
- Use mock tools until official Swiggy MCP access is approved.

## Safety Rules

- Never place a real order automatically.
- Never checkout unless `user_confirmation=true`.
- Never store card/payment information.
- Never log OAuth tokens, session tokens, authorization headers, phone numbers, OTPs, or full addresses.
- Never scrape Swiggy.
- Never reverse engineer Swiggy private APIs.
- Never misrepresent prices, availability, discounts, or delivery time.

## Initial Mock Tools

- `search_food`
- `search_instamart_items`
- `create_cart`
- `add_item_to_cart`
- `remove_item_from_cart`
- `review_cart`
- `apply_coupon_mock`
- `confirm_checkout_mock`
- `track_order_mock`

## Expected Future Backend Structure

Do not create this backend code yet. When implementation begins, use a structure similar to:

```text
backend/
  app/
    main.py
    api/
      routes/
        health.py
        assistant.py
        cart.py
        orders.py
    services/
      intent_service.py
      policy_service.py
      cart_service.py
      order_service.py
    adapters/
      swiggy_mcp_adapter.py
      mock_swiggy_tools.py
    models/
      requests.py
      responses.py
      cart.py
    core/
      config.py
      logging.py
      security.py
  tests/
    test_policy_service.py
    test_cart_service.py
    test_mock_tools.py
```

## Implementation Notes

- Keep prompts advisory; enforce safety in backend policy checks.
- Treat mock prices, availability, discounts, and delivery estimates as mock data.
- When real MCP integration is enabled, source prices, availability, delivery estimates, and discounts from Swiggy MCP responses.
- Keep logs useful but non-sensitive.
