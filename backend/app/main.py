from fastapi import FastAPI

from app.api.routes import assistant, cart, food, health, instamart, orders
from app.core.config import get_settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Mock-first Swiggy ordering assistant backend.",
    )
    app.include_router(health.router)
    app.include_router(assistant.router, prefix="/api/v1")
    app.include_router(cart.router, prefix="/api/v1")
    app.include_router(food.router, prefix="/api/v1")
    app.include_router(instamart.router, prefix="/api/v1")
    app.include_router(orders.router, prefix="/api/v1")
    return app


app = create_app()
