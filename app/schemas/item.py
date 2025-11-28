"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    """Base schema for Item."""

    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating an Item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating an Item."""

    name: Optional[str] = None
    description: Optional[str] = None


class ItemResponse(ItemBase):
    """Schema for Item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
