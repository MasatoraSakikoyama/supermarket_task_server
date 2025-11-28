"""Routers package."""

from app.routers.shop_settlements import router as shop_settlements_router
from app.routers.shops import router as shops_router

__all__ = ["shops_router", "shop_settlements_router"]
