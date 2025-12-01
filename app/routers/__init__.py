"""Routers package."""

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.shop_settlements import router as shop_settlements_router
from app.routers.shops import router as shops_router

__all__ = ["shops_router", "shop_settlements_router", "auth_router", "health_router"]
