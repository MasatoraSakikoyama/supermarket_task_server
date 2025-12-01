"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    aws_region: str = ""

    # Database settings for AWS Aurora MySQL
    database_url: str = ""

    # DynamoDB settings
    dynamodb_endpoint_url: str = ""
    dynamodb_table_name: str = ""

    # JWT settings
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
