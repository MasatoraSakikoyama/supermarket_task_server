"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    """Base schema for Shop."""

    region_id: int
    area_id: int
    prefecture_id: int
    name: str = Field(..., max_length=255)


class ShopCreate(ShopBase):
    """Schema for creating a Shop."""

    pass


class ShopUpdate(BaseModel):
    """Schema for updating a Shop."""

    region_id: Optional[int] = None
    area_id: Optional[int] = None
    prefecture_id: Optional[int] = None
    name: Optional[str] = None


class ShopResponse(ShopBase):
    """Schema for Shop response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
