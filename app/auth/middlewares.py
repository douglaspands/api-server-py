"""Auth Middlewares."""
from jose import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.users import services as user_service
from app.config import settings
from app.users.models import User as UserModel
from app.core.exceptions.http import HttpForbiddenError, HttpUnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}{settings.AUTH_TOKEN_URL}')


async def check_authentication(token: str = Depends(oauth2_scheme)) -> UserModel:
    """Check authentication user.

    Args:
        token (str, optional): Current token. Defaults to Depends(oauth2_scheme).

    Raises:
        HttpUnauthorizedError: Unauthorized access.
        HttpForbiddenError: Inactive user.

    Returns:
        UserModel: User data.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = await user_service.get_user(username=payload.get('sub'))

    except BaseException:
        raise HttpUnauthorizedError('Could not validate credentials')

    if not user.is_active:
        raise HttpForbiddenError(message='Inactive user')

    return user


__all__ = ('check_authentication',)
