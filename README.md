# Swiggy InstaOrder AI

Swiggy InstaOrder AI is a mock-first personal AI ordering assistant prototype designed to work with Swiggy MCP Food and Instamart workflows.

The goal is to help users discover food and grocery options, prepare carts, review items, and complete checkout only after explicit user confirmation.

This repository currently contains the architecture, safety rules, and implementation plan. Real Swiggy MCP calls will be added only after official access approval.

## Use Case

A user can ask natural language requests such as:

- "Order my usual evening snacks."
- "Find healthy dinner options under ₹300."
- "Add milk, eggs, bread, and fruits to my Instamart cart."
- "Show me high-protein snacks available nearby."
- "Track my last order."

The assistant will understand the request, call backend services, prepare a suggested cart, show a review summary, and ask the user for confirmation before checkout.

## Planned MCP Servers

The first version is planned for:

- Swiggy Food MCP
- Swiggy Instamart MCP

Dineout may be added later if the use case expands to table booking.

## Architecture

```text
Client / AI Assistant
        ↓
FastAPI Backend
        ↓
Intent + Policy + Cart Orchestration
        ↓
Swiggy MCP Adapter
        ↓
Swiggy Food MCP / Swiggy Instamart MCP
