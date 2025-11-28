"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SettlementBase(BaseModel):
    """Base schema for Settlement."""

    name: str
    description: Optional[str] = None


class SettlementCreate(SettlementBase):
    """Schema for creating a Settlement."""

    pass


class SettlementUpdate(BaseModel):
    """Schema for updating a Settlement."""

    name: Optional[str] = None
    description: Optional[str] = None


class SettlementResponse(SettlementBase):
    """Schema for Settlement response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
