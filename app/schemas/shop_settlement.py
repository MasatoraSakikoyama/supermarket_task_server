"""Pydantic schemas for shop settlement request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShopSettlementBase(BaseModel):
    """Base schema for ShopSettlement."""

    name: str
    description: Optional[str] = None


class ShopSettlementCreate(ShopSettlementBase):
    """Schema for creating a ShopSettlement."""

    pass


class ShopSettlementUpdate(BaseModel):
    """Schema for updating a ShopSettlement."""

    name: Optional[str] = None
    description: Optional[str] = None


class ShopSettlementResponse(ShopSettlementBase):
    """Schema for ShopSettlement response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    created_at: datetime
    updated_at: datetime
