from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.orm import relationship


from app.consts import AccountPeriodType
from app.models.types import IntEnumType
from app.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
    )
    period_type = Column(
        IntEnumType(AccountPeriodType),
        nullable=False,
        index=True,
    )
    is_cumulative = Column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    shop_account_titles = relationship("ShopAccountTitle", back_populates="shop", cascade="all, delete-orphan")
    shop_account_entries = relationship("ShopAccountEntry", back_populates="shop", cascade="all, delete-orphan")
