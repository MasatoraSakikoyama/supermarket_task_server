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


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to Supermarket Task Server API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# AWS Lambda handler using Mangum
handler = Mangum(app)
