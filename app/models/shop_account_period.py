from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.const import AccountPeriod, CountType
from app.database import Base


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
    month = Column(
        Integer,
        nullable=False,
        index=True,
    )
    period = Column(
        Enum(AccountPeriod),
        nullable=False,
        index=True,
    )
    count_type = Column(
        Enum(CountType),
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

    shop = relationship("Shop", backref="shop_account_periods")
