"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShopAccountEntry(BaseModel):
    """Base schema for ShopAccountEntry."""

    id: Optional[int] = None
    shop_id: int
    shop_account_title_id: Optional[int] = None
    year: int
    month: int
    amount: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ShopAccountEntryRequest(BaseModel):
    """Schema for creating a ShopAccountEntry."""

    year: int
    revenues: list[list[ShopAccountEntry]]
    expenses: list[list[ShopAccountEntry]]


class ShopAccountEntryResponse(BaseModel):
    """Schema for ShopAccountEntry response."""

    headers: list[str]
    revenues: list[list[ShopAccountEntry]]
    expenses: list[list[ShopAccountEntry]]

