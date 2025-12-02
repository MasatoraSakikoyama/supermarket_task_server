"""Pydantic schemas for shop request/response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.consts import AccountTitleType, AccountTitleSubType


class ShopAccountTitleBase(BaseModel):
    """Base schema for ShopAccountTitle."""

    shop_id: int
    type: AccountTitleType
    sub_type: AccountTitleSubType
    code: str | None = Field(None, max_length=50)
    name: str = Field(..., max_length=255)
    order: int


class ShopAccountTitleCreate(ShopAccountTitleBase):
    """Schema for creating a ShopAccountTitle."""

    pass

class ShopAccountTitleUpdate(BaseModel):
    """Schema for updating a ShopAccountTitle."""

    id: int
    type: AccountTitleType | None = None
    sub_type: AccountTitleSubType | None = None
    code: str | None = Field(None, max_length=50)
    name: str | None = Field(None, max_length=255)
    order: int | None = None


class ShopAccountTitleResponse(ShopAccountTitleBase):
    """Schema for ShopAccountTitle response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
