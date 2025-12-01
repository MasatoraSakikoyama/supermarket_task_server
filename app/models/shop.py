from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.const import AccountPeriod
from app.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    region = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False,
        index=True,
    )
    area = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=False,
        index=True,
    )
    prefecture = Column(
        Integer,
        ForeignKey("prefectures.id"),
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ShopAccountPeriod(Base):
    __tablename__ = "shop_account_periods"

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
    year = Column(
        Integer,
        nullable=False,
        index=True,
    )
    period = Column(
        Enum(AccountPeriod),
        nullable=False,
        index=True,
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

    shop = relationship("Shop", backref="shop_account_periods")


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
    account_title_id = Column(
        Integer,
        ForeignKey("account_titles.id"),
        nullable=False,
        index=True,
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

    shop = relationship("Shop", backref="shop_account_titles")
    account_title = relationship("AccountTitle")


class ShopAccountSettlement(Base):
    __tablename__ = "shop_account_settlements"

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
    shop_account_period_id = Column(
        Integer,
        ForeignKey("shop_account_periods.id"),
        nullable=False,
        index=True,
    )
    shop_account_title_id = Column(
        Integer,
        ForeignKey("shop_account_titles.id"),
        nullable=False,
        index=True,
    )
    amount = Column(
        DECIMAL(precision=12, scale=2),
        nullable=False,
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

    shop = relationship("Shop", backref="shop_account_settlements")
