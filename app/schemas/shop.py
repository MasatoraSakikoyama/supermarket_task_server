"""Pydantic schemas for shop request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.const import AccountPeriod


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


class ShopAccountPeriodBase(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    period: AccountPeriod


class ShopAccountPeriodCreate(ShopAccountPeriodBase):
    """Schema for creating a ShopAccountPeriod."""

    pass


class ShopAccountPeriodUpdate(BaseModel):
    """Schema for updating a ShopAccountPeriod."""

    year: Optional[int] = Field(None, ge=2000, le=2100)
    period: Optional[AccountPeriod] = None


class ShopAccountPeriodResponse(ShopAccountPeriodBase):
    """Schema for ShopAccountPeriod response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    year: int
    period: AccountPeriod
    created_at: datetime
    updated_at: datetime


class ShopAccountTitleBase(BaseModel):
    """Base schema for ShopAccountTitle."""

    shop_id: int
    account_title_id: int


class ShopAccountTitleCreate(ShopAccountTitleBase):
    """Schema for creating a ShopAccountTitle."""

    pass


class ShopAccountTitleResponse(ShopAccountTitleBase):
    """Schema for ShopAccountTitle response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ShopAccountSettlementBase(BaseModel):
    """Base schema for ShopAccountSettlement."""

    shop_id: int
    shop_account_period_id: int
    shop_account_title_id: int
    amount: float


class ShopAccountSettlementCreate(ShopAccountSettlementBase):
    """Schema for creating a ShopAccountSettlement."""

    pass


class ShopAccountSettlementUpdate(BaseModel):
    """Schema for updating a ShopAccountSettlement."""

    amount: Optional[float] = None


class ShopAccountSettlementResponse(ShopAccountSettlementBase):
    """Schema for ShopAccountSettlement response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shop_id: int
    shop_account_period_id: int
    shop_account_title_id: int
    amount: float
    created_at: datetime
    updated_at: datetime
