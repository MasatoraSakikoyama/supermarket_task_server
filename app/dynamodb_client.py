"""DynamoDB connection and token storage."""

import time
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings

settings = get_settings()

# DynamoDB resource (singleton)
_dynamodb_resource = None


def get_dynamodb_resource():
    """Get DynamoDB resource (singleton)."""
    global _dynamodb_resource
    if _dynamodb_resource is None:
        if settings.dynamodb_endpoint_url:
            _dynamodb_resource = boto3.resource(
                "dynamodb",
                region_name=settings.dynamodb_region,
                endpoint_url=settings.dynamodb_endpoint_url,
            )
        else:
            _dynamodb_resource = boto3.resource(
                "dynamodb",
                region_name=settings.dynamodb_region,
            )
    return _dynamodb_resource


def get_token_table():
    """Get DynamoDB table for token storage."""
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(settings.dynamodb_table_name)


def store_token(user_id: int, token: str, expire_seconds: int) -> bool:
    """Store token in DynamoDB with expiration (TTL)."""
    table = get_token_table()
    ttl = int(time.time()) + expire_seconds
    try:
        table.put_item(
            Item={
                "user_id": str(user_id),
                "token": token,
                "ttl": ttl,
            }
        )
        return True
    except ClientError:
        return False


def get_stored_token(user_id: int) -> Optional[str]:
    """Get stored token for user from DynamoDB."""
    table = get_token_table()
    try:
        response = table.get_item(Key={"user_id": str(user_id)})
        item = response.get("Item")
        if item:
            # Check if token has expired (in case TTL hasn't cleaned it up yet)
            ttl = item.get("ttl", 0)
            if ttl > int(time.time()):
                return item.get("token")
        return None
    except ClientError:
        return None


def delete_token(user_id: int) -> bool:
    """Delete token from DynamoDB."""
    table = get_token_table()
    try:
        table.delete_item(Key={"user_id": str(user_id)})
        return True
    except ClientError:
        return False


def is_token_valid(user_id: int, token: str) -> bool:
    """Check if the provided token matches the stored token."""
    stored_token = get_stored_token(user_id)
    return stored_token == token
