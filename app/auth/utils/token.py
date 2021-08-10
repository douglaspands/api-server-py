"""Auth Utils."""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from jose import jwt

from app.config import settings


async def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create access token.

    Args:
        data (Dict[str, Any]): Data to encode.
        expires_delta (Optional[timedelta], optional): Seconds to expired. Defaults to None.

    Returns:
        str: JWT encoded.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


__all__ = ("create_access_token",)
