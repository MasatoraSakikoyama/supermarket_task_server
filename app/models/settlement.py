"""SQLAlchemy models for the application."""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class Settlement(Base):
    """Example settlement model for demonstration."""

    __tablename__ = "settlements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
