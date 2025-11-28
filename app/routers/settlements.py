"""Settlement router for CRUD operations."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.settlement import Settlement
from app.schemas.settlement import SettlementCreate, SettlementResponse, SettlementUpdate

router = APIRouter(prefix="/settlements", tags=["settlements"])


@router.get("/", response_model=List[SettlementResponse])
def get_settlements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all settlements with pagination."""
    settlements = db.query(Settlement).offset(skip).limit(limit).all()
    return settlements


@router.get("/{settlement_id}", response_model=SettlementResponse)
def get_settlement(settlement_id: int, db: Session = Depends(get_db)):
    """Get a single settlement by ID."""
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settlement not found"
        )
    return settlement


@router.post("/", response_model=SettlementResponse, status_code=status.HTTP_201_CREATED)
def create_settlement(settlement_data: SettlementCreate, db: Session = Depends(get_db)):
    """Create a new settlement."""
    settlement = Settlement(**settlement_data.model_dump())
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement


@router.put("/{settlement_id}", response_model=SettlementResponse)
def update_settlement(settlement_id: int, settlement_data: SettlementUpdate, db: Session = Depends(get_db)):
    """Update an existing settlement."""
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settlement not found"
        )

    update_data = settlement_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settlement, field, value)

    db.commit()
    db.refresh(settlement)
    return settlement


@router.delete("/{settlement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_settlement(settlement_id: int, db: Session = Depends(get_db)):
    """Delete a settlement."""
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if settlement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settlement not found"
        )
    db.delete(settlement)
    db.commit()
    return None
