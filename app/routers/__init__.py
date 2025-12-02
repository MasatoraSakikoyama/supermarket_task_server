"""Routers package."""

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.shop import router as shop_router
from app.routers.shop_account_entry import router as shop_account_entry_router
from app.routers.shop_account_title import router as shop_account_title_router


__all__ = [
    "auth_router",
    "health_router",
    "shop_router",
    "shop_account_entry_router",
    "shop_account_title_router",
]
