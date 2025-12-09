from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.consts import AccountTitleType, AccountTitleSubType
from app.models.types import IntEnumType
from app.database import Base


class ShopAccountTitle(Base):
    __tablename__ = "shop_account_titles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    shop_id = Column(
        Integer,
        ForeignKey("shops.id"),
        nullable=False,
        index=True,
    )
    type = Column(
        IntEnumType(AccountTitleType),
        nullable=False,
        index=True,
    )
    sub_type = Column(
        IntEnumType(AccountTitleSubType),
        nullable=False,
        index=True,
    )
    code = Column(
        String(50),
        nullable=True,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
    )
    order = Column(
        Integer,
        nullable=False,
        default=0,
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

    shop = relationship("Shop", back_populates="shop_account_titles")
    shop_account_entries = relationship("ShopAccountEntry", back_populates="shop_account_title", cascade="all, delete-orphan")
