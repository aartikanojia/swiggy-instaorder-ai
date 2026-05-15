from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Swiggy InstaOrder AI"
    app_version: str = "0.1.0"
    mode: str = "mock"
    log_level: str = "INFO"
    swiggy_food_mcp_url: str = "https://mcp.swiggy.com/food"
    swiggy_instamart_mcp_url: str = "https://mcp.swiggy.com/im"
    real_checkout_enabled: bool = False

    model_config = SettingsConfigDict(env_prefix="INSTAORDER_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
