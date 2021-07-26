from typing import Optional
from datetime import datetime, timedelta

from jose import jwt

from app.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token.

    Args:
        data (dict): Data to encode.
        expires_delta (Optional[timedelta], optional): Seconds to expired. Defaults to None.

    Returns:
        str: JWT encoded.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


__all__ = ('create_access_token',)
