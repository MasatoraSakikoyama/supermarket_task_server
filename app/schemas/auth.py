"""Pydantic schemas for authentication request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class AccountBase(BaseModel):
    """Base schema for Account."""

    username: str
    email: EmailStr


class AccountCreate(AccountBase):
    """Schema for creating an Account."""

    password: str


class AccountResponse(AccountBase):
    """Schema for Account response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""

    account_id: Optional[int] = None
    username: Optional[str] = None
