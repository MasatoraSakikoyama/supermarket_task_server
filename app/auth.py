"""Authentication module with JWT token handling."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.account import Account
from app.redis_client import is_token_valid
from app.schemas.auth import TokenData

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        account_id: int = payload.get("sub")
        username: str = payload.get("username")
        if account_id is None:
            return None
        return TokenData(account_id=account_id, username=username)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authenticate_account(db: Session, username: str, password: str) -> Optional[Account]:
    """Authenticate an account by username and password."""
    account = db.query(Account).filter(Account.username == username).first()
    if not account:
        # Use dummy hash to prevent timing attacks
        pwd_context.verify("dummy_password", get_password_hash("dummy_hash"))
        return None
    if not verify_password(password, account.hashed_password):
        return None
    return account


def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Account:
    """Get current authenticated account from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    token_data = decode_access_token(token)

    if token_data is None or token_data.account_id is None:
        raise credentials_exception

    # Verify token is stored in Redis (not revoked)
    if not is_token_valid(token_data.account_id, token):
        raise credentials_exception

    account = db.query(Account).filter(Account.id == token_data.account_id).first()
    if account is None:
        raise credentials_exception

    return account
