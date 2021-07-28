"""Auth Middlewares."""
from fastapi import Depends

from app.users.models import User
from app.auth.services import get_current_user
from app.core.exceptions.http import HTTPException


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user.

    Args:
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: Inactive user.

    Returns:
        User: User data.
    """
    if current_user.is_active is False:
        raise HTTPException(status_code=400, message='Inactive user')
    return current_user


__all__ = ('get_current_active_user',)
