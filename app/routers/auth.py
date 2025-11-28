"""Authentication router for login and registration."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import (
    authenticate_account,
    create_access_token,
    get_current_account,
    get_password_hash,
)
from app.config import get_settings
from app.database import get_db
from app.models.account import Account
from app.redis_client import delete_token, store_token
from app.schemas.auth import AccountCreate, AccountResponse, LoginRequest, TokenResponse

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def register(account_data: AccountCreate, db: Session = Depends(get_db)):
    """Register a new account."""
    # Check if username already exists
    existing_account = db.query(Account).filter(Account.username == account_data.username).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email already exists
    existing_email = db.query(Account).filter(Account.email == account_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new account
    hashed_password = get_password_hash(account_data.password)
    account = Account(
        username=account_data.username,
        email=account_data.email,
        hashed_password=hashed_password,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token."""
    account = authenticate_account(db, login_data.username, login_data.password)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": account.id, "username": account.username},
        expires_delta=access_token_expires,
    )

    # Store token in Redis
    expire_seconds = settings.jwt_access_token_expire_minutes * 60
    store_token(account.id, access_token, expire_seconds)

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_account: Account = Depends(get_current_account)):
    """Logout and invalidate token."""
    delete_token(current_account.id)
    return None


@router.get("/me", response_model=AccountResponse)
def get_me(current_account: Account = Depends(get_current_account)):
    """Get current account information."""
    return current_account
