"""FastAPI application for AWS Lambda with Mangum adapter."""

from fastapi import FastAPI
from mangum import Mangum

from app.config import get_settings
from app.routers import (
    auth_router,
    health_router,
    shop_account_entry_router,
    shop_router,
)

settings = get_settings()

app = FastAPI(
    title="Supermarket Task Server",
    description="Supermarket Task Server API",
    version="1.0.0",
)

# Include routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(shop_router)
app.include_router(shop_account_entry_router)

# AWS Lambda handler using Mangum
handler = Mangum(app)
