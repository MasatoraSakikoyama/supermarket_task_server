from sqlalchemy import Column, DateTime, Enum, Integer, String, func

from app.const import AccountType
from app.database import Base


class AccountTitle(Base):
    __tablename__ = "account_names"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    type = Column(
        Enum(AccountType),
        nullable=False,
        index=True,
    )
    code = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )
    name = Column(
        String(255),
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
