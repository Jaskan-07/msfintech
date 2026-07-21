"""
Security utilities for authentication
"""
from datetime import datetime, timedelta
from typing import Optional


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against stored password"""
    return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token"""
    return data.get("sub", "")