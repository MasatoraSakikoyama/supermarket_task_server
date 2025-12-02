"""ShopAccountData router for CRUD operations."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Shop, ShopAccountData, User
from app.schemas import (
    ShopAccountDataCreate,
    ShopAccountDataResponse,
    ShopAccountDataUpdate,
)

router = APIRouter(
    prefix="/shop/{shop_id}/account_data",
    tags=["shop_account_data"],
)


@router.get("", response_model=List[ShopAccountDataResponse])
def get_shop_account_data_list(
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
        db.query(ShopAccountData)
        .filter(ShopAccountData.shop_id == shop_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return data


@router.get("/{data_id}", response_model=ShopAccountDataResponse)
def get_shop_account_data(
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
        db.query(ShopAccountData)
        .filter(
            ShopAccountData.id == data_id,
            ShopAccountData.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountData not found",
        )
    return data


@router.post(
    "",
    response_model=ShopAccountDataResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shop_account_data(
    shop_id: int,
    data_data: ShopAccountDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = ShopAccountData(
        shop_id=shop_id,
        **data_data.model_dump(),
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.put("/{data_id}", response_model=ShopAccountDataResponse)
def update_shop_account_data(
    shop_id: int,
    data_id: int,
    data_data: ShopAccountDataUpdate,
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
        db.query(ShopAccountData)
        .filter(
            ShopAccountData.id == data_id,
            ShopAccountData.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountData not found",
        )

    update_data = data_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(data, field, value)

    db.commit()
    db.refresh(data)
    return data


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop_account_data(
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
        db.query(ShopAccountData)
        .filter(
            ShopAccountData.id == data_id,
            ShopAccountData.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountData not found",
        )
    db.delete(data)
    db.commit()
    return None
