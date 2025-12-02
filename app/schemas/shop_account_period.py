"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.const import AccountPeriod, CountType


class ShopAccountPeriodBase(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    period: AccountPeriod


class ShopAccountPeriodCreate(ShopAccountPeriodBase):
    """Schema for creating a ShopAccountPeriod."""

    pass


class ShopAccountPeriodUpdate(BaseModel):
    """Schema for updating a ShopAccountPeriod."""

    id: int
    year: Optional[int] = Field(None, ge=2000, le=2100)
    month: Optional[int] = Field(None, ge=1, le=12)
    period: Optional[AccountPeriod] = None
    count_type: Optional[CountType] = None


class ShopAccountPeriodResponse(ShopAccountPeriodBase):
    """Schema for ShopAccountPeriod response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    year: int
    month: int
    period: AccountPeriod
    created_at: datetime
    updated_at: datetime
