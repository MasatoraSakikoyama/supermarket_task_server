"""ShopAccountEntry router for CRUD operations."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Shop, ShopAccountEntry, User
from app.schemas import (
    ShopAccountEntryCreate,
    ShopAccountEntryResponse,
    ShopAccountEntryUpdate,
)

router = APIRouter(
    prefix="/shop/{shop_id}/account_entry",
    tags=["shop_account_entry"],
)


@router.get("", response_model=List[ShopAccountEntryResponse])
def get_shop_account_entry_list(
    shop_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all data for a shop with pagination."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = (
        db.query(ShopAccountEntry)
        .filter(ShopAccountEntry.shop_id == shop_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return data


@router.get("/{data_id}", response_model=ShopAccountEntryResponse)
def get_shop_account_entry(
    shop_id: int,
    data_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single data by ID for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = (
        db.query(ShopAccountEntry)
        .filter(
            ShopAccountEntry.id == data_id,
            ShopAccountEntry.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountEntry not found",
        )
    return data


@router.post(
    "",
    response_model=ShopAccountEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shop_account_entry(
    shop_id: int,
    data_data: ShopAccountEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = ShopAccountEntry(
        shop_id=shop_id,
        **data_data.model_dump(),
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.put("/{data_id}", response_model=ShopAccountEntryResponse)
def update_shop_account_entry(
    shop_id: int,
    data_id: int,
    data_data: ShopAccountEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = (
        db.query(ShopAccountEntry)
        .filter(
            ShopAccountEntry.id == data_id,
            ShopAccountEntry.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountEntry not found",
        )

    update_data = data_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(data, field, value)

    db.commit()
    db.refresh(data)
    return data


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop_account_entry(
    shop_id: int,
    data_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = (
        db.query(ShopAccountEntry)
        .filter(
            ShopAccountEntry.id == data_id,
            ShopAccountEntry.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountEntry not found",
        )
    db.delete(data)
    db.commit()
    return None
