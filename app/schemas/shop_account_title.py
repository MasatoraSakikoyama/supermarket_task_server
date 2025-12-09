"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.consts import AccountTitleType, AccountTitleSubType


class ShopAccountTitle(BaseModel):
    """Base schema for ShopAccountTitle."""

    id: Optional[int] = None
    shop_id: int
    type: AccountTitleType
    sub_type: AccountTitleSubType
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=255)
    order: int

    model_config = ConfigDict(from_attributes=True)


class ShopAccountTitleRequest(BaseModel):
    """Schema for ShopAccountTitle response."""

    revenues: list[ShopAccountTitle]
    expenses: list[ShopAccountTitle]


class ShopAccountTitleResponse(BaseModel):
    """Schema for ShopAccountTitle response."""

    revenues: list[ShopAccountTitle]
    expenses: list[ShopAccountTitle]
