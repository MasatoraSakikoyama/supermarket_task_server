from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.consts import AccountTitleType
from app.database import get_db
from app.models import Shop, ShopAccountTitle, User
from app.schemas import (
    ShopAccountTitleCreate,
    ShopAccountTitleListResponse,
    ShopAccountTitleResponse,
    ShopAccountTitleUpdate,
)

router = APIRouter(
    prefix="/shop/{shop_id}/account_title",
    tags=["shop_account_title"],
)


@router.get("", response_model=ShopAccountTitleListResponse)
def get_shop_account_title_list(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all data for a shop, grouped by type."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    revenues = (
        db.query(ShopAccountTitle)
        .filter(
            ShopAccountTitle.shop_id == shop_id,
            ShopAccountTitle.type == AccountTitleType.REVENUE,
        )
        .order_by(ShopAccountTitle.order)
        .all()
    )
    expenses = (
        db.query(ShopAccountTitle)
        .filter(
            ShopAccountTitle.shop_id == shop_id,
            ShopAccountTitle.type == AccountTitleType.EXPENSE,
        )
        .order_by(ShopAccountTitle.order)
        .all()
    )
    return ShopAccountTitleListResponse(revenues=revenues, expenses=expenses)


@router.get("/{data_id}", response_model=ShopAccountTitleResponse)
def get_shop_account_title(
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
        db.query(ShopAccountTitle)
        .filter(
            ShopAccountTitle.id == data_id,
            ShopAccountTitle.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountTitle not found",
        )
    return data


@router.post(
    "",
    response_model=ShopAccountTitleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shop_account_title(
    shop_id: int,
    data_data: ShopAccountTitleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    data = ShopAccountTitle(
        shop_id=shop_id,
        **data_data.model_dump(),
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.put("/{data_id}", response_model=ShopAccountTitleResponse)
def update_shop_account_title(
    shop_id: int,
    data_id: int,
    data_data: ShopAccountTitleUpdate,
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
        db.query(ShopAccountTitle)
        .filter(
            ShopAccountTitle.id == data_id,
            ShopAccountTitle.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountTitle not found",
        )

    update_data = data_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(data, field, value)

    db.commit()
    db.refresh(data)
    return data


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop_account_title(
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
        db.query(ShopAccountTitle)
        .filter(
            ShopAccountTitle.id == data_id,
            ShopAccountTitle.shop_id == shop_id,
        )
        .first()
    )
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ShopAccountTitle not found",
        )
    db.delete(data)
    db.commit()
    return None
