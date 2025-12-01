from enum import IntEnum


class AccountPeriod(IntEnum):
    MONTHLY = 1  # 月次
    QUARTERLY = 2  # 四半期
    SEMI_ANNUAL = 3  # 半期
    YEARLY = 4 # 年次


class AccountType(IntEnum):
    REVENUE = 4  # 収益
    EXPENSE = 5  # 費用
