"""Application configuration using pydantic-settings."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")

    # Database settings for AWS Aurora MySQL
    db_host: str = ""
    db_port: int = 3306
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

    # DynamoDB settings
    dynamodb_table_name: str = ""
    dynamodb_region: str = ""
    dynamodb_endpoint_url: str = ""

    # JWT settings
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    @property
    def database_url(self) -> str:
        """Generate SQLAlchemy database URL for Aurora MySQL."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
