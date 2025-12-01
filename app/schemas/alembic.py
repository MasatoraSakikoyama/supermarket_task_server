"""Pydantic schemas for Alembic command API request/response validation."""

from typing import Optional

from pydantic import BaseModel, Field


class AlembicUpgradeRequest(BaseModel):
    """Schema for alembic upgrade request."""

    revision: str = Field(
        default="head",
        description="Target revision to upgrade to (default: 'head')",
    )


class AlembicDowngradeRequest(BaseModel):
    """Schema for alembic downgrade request."""

    revision: str = Field(
        description="Target revision to downgrade to (e.g., '-1' for one step back)",
    )


class AlembicRevisionRequest(BaseModel):
    """Schema for creating a new alembic revision."""

    message: str = Field(description="Revision message")
    autogenerate: bool = Field(
        default=True,
        description="Whether to autogenerate the migration script",
    )


class AlembicResponse(BaseModel):
    """Schema for alembic command response."""

    success: bool
    message: str
    output: Optional[str] = None


class AlembicCurrentResponse(BaseModel):
    """Schema for alembic current command response."""

    success: bool
    current_revision: Optional[str] = None
    message: str


class AlembicHistoryItem(BaseModel):
    """Schema for a single revision in history."""

    revision: str
    down_revision: Optional[str] = None
    message: Optional[str] = None


class AlembicHistoryResponse(BaseModel):
    """Schema for alembic history command response."""

    success: bool
    revisions: list[AlembicHistoryItem]
    message: str
