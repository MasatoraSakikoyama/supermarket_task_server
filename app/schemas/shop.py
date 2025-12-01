"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShopBase(BaseModel):
    """Base schema for Shop."""

    name: str
    description: Optional[str] = None


class ShopCreate(ShopBase):
    """Schema for creating a Shop."""

    pass


class ShopUpdate(BaseModel):
    """Schema for updating a Shop."""

    name: Optional[str] = None
    description: Optional[str] = None


class ShopResponse(ShopBase):
    """Schema for Shop response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ShopAccountSettlementBase(BaseModel):
    """Base schema for ShopAccountSettlement."""

    name: str
    description: Optional[str] = None


class ShopAccountSettlementCreate(ShopAccountSettlementBase):
    """Schema for creating a ShopAccountSettlement."""

    pass


class ShopAccountSettlementUpdate(BaseModel):
    """Schema for updating a ShopAccountSettlement."""

    name: Optional[str] = None
    description: Optional[str] = None


class ShopAccountSettlementResponse(ShopAccountSettlementBase):
    """Schema for ShopAccountSettlement response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    created_at: datetime
    updated_at: datetime
