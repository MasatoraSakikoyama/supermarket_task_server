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
