"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShopAccountDataBase(BaseModel):
    """Base schema for ShopAccountData."""

    shop_id: int
    shop_account_period_id: int
    shop_account_title_id: int
    amount: float


class ShopAccountDataCreate(ShopAccountDataBase):
    """Schema for creating a ShopAccountData."""

    pass


class ShopAccountDataUpdate(BaseModel):
    """Schema for updating a ShopAccountData."""

    id: int
    amount: Optional[float] = None


class ShopAccountDataResponse(ShopAccountDataBase):
    """Schema for ShopAccountData response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    shop_account_period_id: int
    shop_account_title_id: int
    amount: float
    created_at: datetime
    updated_at: datetime
