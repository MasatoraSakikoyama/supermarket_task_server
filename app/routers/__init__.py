"""Routers package."""

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.shop import router as shop_router
from app.routers.shop_account_data import router as shop_account_data_router

__all__ = [
    "shop_router",
    "shop_account_data_router",
    "auth_router",
    "health_router",
]
