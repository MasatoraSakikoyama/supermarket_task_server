from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Region(Base):
    __tablename__ = "regions"

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
    code = Column(
        String(50),
        nullable=False,
        unique=True,
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


class Area(Base):
    __tablename__ = "areas"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    region_id = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
    )
    code = Column(
        String(50),
        nullable=False,
        unique=True,
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

    region = relationship("Region", backref="areas")


class Prefecture(Base):
    __tablename__ = "prefectures"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    area_id = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
    )
    code = Column(
        String(50),
        nullable=False,
        unique=True,
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

    area = relationship("Area", backref="prefectures")
