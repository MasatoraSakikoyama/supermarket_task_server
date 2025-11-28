"""ShopSettlement router for CRUD operations."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shop import Shop
from app.models.shop_settlement import ShopSettlement
from app.schemas.shop_settlement import (
    ShopSettlementCreate,
    ShopSettlementResponse,
    ShopSettlementUpdate,
)

router = APIRouter(prefix="/shops/{shop_id}/settlements", tags=["shop_settlements"])


@router.get("/", response_model=List[ShopSettlementResponse])
def get_shop_settlements(
    shop_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all settlements for a shop with pagination."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    settlements = (
        db.query(ShopSettlement)
        .filter(ShopSettlement.shop_id == shop_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return settlements


@router.get("/{settlement_id}", response_model=ShopSettlementResponse)
def get_shop_settlement(shop_id: int, settlement_id: int, db: Session = Depends(get_db)):
    """Get a single settlement by ID for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    settlement = (
        db.query(ShopSettlement)
        .filter(ShopSettlement.id == settlement_id, ShopSettlement.shop_id == shop_id)
        .first()
    )
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ShopSettlement not found"
        )
    return settlement


@router.post("/", response_model=ShopSettlementResponse, status_code=status.HTTP_201_CREATED)
def create_shop_settlement(
    shop_id: int, settlement_data: ShopSettlementCreate, db: Session = Depends(get_db)
):
    """Create a new settlement for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    settlement_dict = settlement_data.model_dump()
    settlement_dict["shop_id"] = shop_id
    settlement = ShopSettlement(**settlement_dict)
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement


@router.put("/{settlement_id}", response_model=ShopSettlementResponse)
def update_shop_settlement(
    shop_id: int,
    settlement_id: int,
    settlement_data: ShopSettlementUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing settlement for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    settlement = (
        db.query(ShopSettlement)
        .filter(ShopSettlement.id == settlement_id, ShopSettlement.shop_id == shop_id)
        .first()
    )
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ShopSettlement not found"
        )

    update_data = settlement_data.model_dump(exclude_unset=True)
    # Remove shop_id from update if present to prevent changing parent
    update_data.pop("shop_id", None)
    for field, value in update_data.items():
        setattr(settlement, field, value)

    db.commit()
    db.refresh(settlement)
    return settlement


@router.delete("/{settlement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop_settlement(shop_id: int, settlement_id: int, db: Session = Depends(get_db)):
    """Delete a settlement for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    settlement = (
        db.query(ShopSettlement)
        .filter(ShopSettlement.id == settlement_id, ShopSettlement.shop_id == shop_id)
        .first()
    )
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ShopSettlement not found"
        )
    db.delete(settlement)
    db.commit()
    return None
