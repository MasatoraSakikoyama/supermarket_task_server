"""FastAPI application for AWS Lambda with Mangum adapter."""

from fastapi import FastAPI
from mangum import Mangum

from app.config import get_settings
from app.routers import auth_router, shop_settlements_router, shops_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Supermarket Task Server API",
    version="1.0.0",
)

# Include routers
app.include_router(auth_router)
app.include_router(shops_router)
app.include_router(shop_settlements_router)


# AWS Lambda handler using Mangum
handler = Mangum(app)
