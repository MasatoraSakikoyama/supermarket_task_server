"""Pydantic schemas for shop request/response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.consts import AccountType


class ShopAccountTitleBase(BaseModel):
    """Base schema for ShopAccountTitle."""

    shop_id: int
    type: AccountType
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)


class ShopAccountTitleCreate(ShopAccountTitleBase):
    """Schema for creating a ShopAccountTitle."""

    pass

class ShopAccountTitleUpdate(BaseModel):
    """Schema for updating a ShopAccountTitle."""

    id: int
    type: AccountType | None = None
    code: str | None = Field(None, max_length=50)
    name: str | None = Field(None, max_length=255)


class ShopAccountTitleResponse(ShopAccountTitleBase):
    """Schema for ShopAccountTitle response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
