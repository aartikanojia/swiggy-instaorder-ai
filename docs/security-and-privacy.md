# Security and Privacy

Swiggy InstaOrder AI follows a confirmation-first and privacy-first approach. The assistant can help prepare a cart, but checkout requires backend validation and explicit user approval.

## Confirmation Rule

Checkout requires `user_confirmation=true`. If confirmation is missing, ambiguous, stale, or not tied to the current cart review, checkout must not execute.

## Allowed Data

- Basic user preferences.
- Mock cart state.
- Mock order state.
- Non-sensitive usage logs.

## Not Allowed Data

- Card details.
- Payment credentials.
- OAuth tokens in logs.
- Session tokens in logs.
- Sensitive user address data in plain logs.

## Source of Truth

When real integration is enabled, prices, availability, delivery estimates, discounts, and offers must come from Swiggy MCP responses. The system must not invent or misrepresent commercial information.

## Forbidden Behaviors

- Scraping.
- Reverse engineering private Swiggy APIs.
- Bypassing MCP access controls.
- Reselling access.
- Hiding Swiggy attribution.
- Misrepresenting price, availability, offer, or delivery time.
- Placing orders without user approval.

## Secrets Rules

- Keep credentials in environment variables or managed secret stores.
- Do not commit secrets, tokens, client IDs, client secrets, OTPs, or API keys.
- Use separate environment configuration for local, staging, and production deployments.
- Rotate credentials immediately if exposure is suspected.

## Logging Rules

- Never log OAuth tokens, session tokens, authorization headers, phone numbers, OTPs, or full addresses.
- Redact sensitive request and response fields before logs are written.
- Prefer event IDs, cart IDs, and mock order IDs over raw user identifiers.
- Keep logs useful for debugging policy decisions without exposing private user data.

## Real Checkout Status

Real checkout remains disabled until official Swiggy MCP access is approved and security checks are complete.
