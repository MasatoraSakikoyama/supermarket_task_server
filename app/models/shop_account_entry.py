from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.database import Base


class ShopAccountEntry(Base):
    __tablename__ = "shop_account_entry"

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
    shop_account_title_id = Column(
        Integer,
        ForeignKey("shop_account_titles.id"),
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

    shop = relationship("Shop", backref="shop_account_entry")
