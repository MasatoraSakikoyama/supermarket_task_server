from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.consts import AccountTitleType
from app.database import get_db
from app.models import Shop, ShopAccountTitle, User
from app.schemas import (
    ShopAccountTitleRequest,
    ShopAccountTitleResponse,
)

router = APIRouter(
    prefix="/shop/{shop_id}/account_title",
    tags=["shop_account_title"],
)


@router.get("", response_model=ShopAccountTitleResponse)
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
    models = (
        db.query(ShopAccountTitle)
        .filter(ShopAccountTitle.shop_id == shop_id)
        .order_by(ShopAccountTitle.type, ShopAccountTitle.order)
        .all()
    )
    revenues = [model for model in models if model.type == AccountTitleType.REVENUE]
    expenses = [model for model in models if model.type == AccountTitleType.EXPENSE]

    return ShopAccountTitleResponse(revenues=revenues, expenses=expenses)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def bulk_delete_and_create_shop_account_title(
    shop_id: int,
    data: ShopAccountTitleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new data for a shop."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )

    (
        db.query(ShopAccountTitle)
        .filter(ShopAccountTitle.shop_id == shop_id)
        .delete()
    )

    models = []
    for data in data.revenues + data.expenses:
        # TODO: data.codeで判定する
        if not data.name:
            continue

        models.append(
            ShopAccountTitle(
                shop_id=shop_id,
                type=data.type,
                sub_type=data.sub_type,
                code=data.code,
                name=data.name,
                order=data.order,
            )
        )

    db.add_all(models)
    db.commit()
