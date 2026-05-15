from app.models.cart import Cart


class PolicyError(ValueError):
    pass


class PolicyService:
    def validate_checkout(self, cart: Cart, user_confirmation: bool) -> None:
        if not user_confirmation:
            raise PolicyError("Checkout requires explicit user_confirmation=true.")
        if not cart.items:
            raise PolicyError("Checkout requires a non-empty reviewed cart.")
        if not cart.mock:
            raise PolicyError("Real checkout is disabled until official Swiggy MCP access is approved.")
