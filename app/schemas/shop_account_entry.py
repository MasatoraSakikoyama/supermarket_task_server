"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShopAccountEntryBase(BaseModel):
    """Base schema for ShopAccountEntry."""

    shop_id: int
    shop_account_title_id: int
    year: int
    month: int
    amount: float


class ShopAccountEntryCreate(ShopAccountEntryBase):
    """Schema for creating a ShopAccountEntry."""

    pass


class ShopAccountEntryUpdate(BaseModel):
    """Schema for updating a ShopAccountEntry."""

    id: int
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[float] = None


class ShopAccountEntryResponse(ShopAccountEntryBase):
    """Schema for ShopAccountEntry response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    shop_account_title_id: int
    year: int
    month: int
    amount: float
    created_at: datetime
    updated_at: datetime
