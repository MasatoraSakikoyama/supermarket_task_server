from enum import IntEnum


class AccountPeriodType(IntEnum):
    MONTHLY = 1  # 月次
    QUARTERLY = 2  # 四半期
    SEMI_ANNUAL = 3  # 半期
    YEARLY = 4  # 年次


class AccountTitleType(IntEnum):
    REVENUE = 1  # 収益
    EXPENSE = 2  # 費用


class AccountTitleSubType(IntEnum):
    SALES = 1  # 売上
    NON_OPERATING_REVENUE = 2  # 営業外収益
    EXTRAORDINARY_INCOME = 3  # 特別利益
    COST_OF_GOODS_SOLD = 100  # 売上原価
    SELLING_GENERAL_ADMINISTRATIVE_EXPENSE = 101  # 販売費及び一般管理費
    NON_OPERATING_EXPENSE = 102  # 営業外費用
    EXTRAORDINARY_LOSS = 103  # 特別損失
