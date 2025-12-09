from typing import List
from collections import OrderedDict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload, contains_eager

from app.consts import AccountPeriodType, AccountTitleType
from app.auth import get_current_user
from app.database import get_db
from app.models import Shop, ShopAccountEntry, User, ShopAccountTitle
from app.schemas import (
    ShopAccountEntryRequest,
    ShopAccountEntryResponse,
)


router = APIRouter(
    prefix="/shop/{shop_id}/account_entry",
    tags=["shop_account_entry"],
)

AccountPeriodMonths = {
    AccountPeriodType.MONTHLY: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    AccountPeriodType.QUARTERLY: [3, 6, 9, 12],
    AccountPeriodType.SEMI_ANNUAL: [6, 12],
    AccountPeriodType.YEARLY: [3],
}


def get_headers(year: int, period_type: AccountPeriodType) -> List[str]:
    months = AccountPeriodMonths[period_type]
    headers = [f"{year}年{month}月" for month in months]
    return headers


@router.get("", response_model=ShopAccountEntryResponse)
def get_shop_account_entry_list(
    shop_id: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all data for a shop with pagination."""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )
    headers = get_headers(year, shop.period_type)

    titles = (
        db.query(ShopAccountTitle)
        .filter(ShopAccountTitle.shop_id == shop_id)
        .order_by(ShopAccountTitle.type, ShopAccountTitle.order)
        .all()
    )
    if len(titles) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop account titles not found"
        )

    revenue_map = OrderedDict()
    expense_map = OrderedDict()
    for title in titles:
        if title.type == AccountTitleType.REVENUE:
            revenue_map.setdefault(title.id, OrderedDict({
                month: {
                    "id": None,
                    "shop_id": shop_id,
                    "shop_account_title_id": title.id,
                    "year": year,
                    "month": month,
                    "amount": None,
                } for month in AccountPeriodMonths[shop.period_type]
            }))
        elif title.type == AccountTitleType.EXPENSE:
            expense_map.setdefault(title.id, OrderedDict({
                month: {
                    "id": None,
                    "shop_id": shop_id,
                    "shop_account_title_id": title.id,
                    "year": year,
                    "month": month,
                    "amount": None,
                } for month in AccountPeriodMonths[shop.period_type]
            }))

    models = (
        db.query(ShopAccountEntry)
        .join(ShopAccountEntry.shop_account_title)
        .filter(ShopAccountEntry.shop_id == shop_id)
        .filter(ShopAccountEntry.year == year)
        .all()
    )
    for model in models:
        if model.shop_account_title.type == AccountTitleType.REVENUE:
            item = revenue_map[model.shop_account_title_id][model.month]
        elif model.shop_account_title.type == AccountTitleType.EXPENSE:
            item = expense_map[model.shop_account_title_id][model.month]

        item["id"] = model.id
        item["shop_account_title_id"] = model.shop_account_title_id
        item["amount"] = model.amount

    revenues = [month_map.values() for month_map in revenue_map.values()]
    expenses = [month_map.values() for month_map in expense_map.values()]

    return ShopAccountEntryResponse(headers=headers, revenues=revenues, expenses=expenses)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def bulk_delete_and_create_shop_account_entry(
    shop_id: int,
    data: ShopAccountEntryRequest,
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
        db.query(ShopAccountEntry)
        .filter(ShopAccountEntry.shop_id == shop_id)
        .filter(ShopAccountEntry.year == data.year)
        .delete()
    )

    models = []
    for item_list in data.revenues +data.expenses:
        for item in item_list:
            if item.amount is None:
                continue

            models.append(
                ShopAccountEntry(
                    shop_id=item.shop_id,
                    shop_account_title_id=item.shop_account_title_id,
                    year=item.year,
                    month=item.month,
                    amount=item.amount,
                )
            )

    db.add_all(models)
    db.commit()
