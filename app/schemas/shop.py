"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.consts import AccountPeriodType


class ShopBase(BaseModel):
    """Base schema for Shop."""

    name: str = Field(..., max_length=255)
    period_type: AccountPeriodType
    is_cumulative: bool


class ShopCreate(ShopBase):
    """Schema for creating a Shop."""

    pass


class ShopUpdate(BaseModel):
    """Schema for updating a Shop."""

    name: Optional[str] = None
    period_type: Optional[AccountPeriodType] = None
    is_cumulative: Optional[bool] = None


class ShopResponse(ShopBase):
    """Schema for Shop response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
