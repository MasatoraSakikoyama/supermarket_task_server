"""Pydantic schemas for authentication request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base schema for User."""

    name: str = Field(..., min_length=3, max_length=255)
    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    """Schema for creating an User."""

    password: str = Field(..., min_length=3, max_length=72)


class UserResponse(UserBase):
    """Schema for User response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=4, max_length=72)


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Schema for login response with token and user info."""

    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class TokenData(BaseModel):
    """Schema for decoded token data."""

    user_id: Optional[int] = None
    user_name: Optional[str] = None
