from typing import Optional
from jose import JWTError, jwt
from users import model, service
from fastapi import Depends, status
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from core.utils.password import verify_password
from core.exception.http import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}{settings.AUTH_TOKEN_URL}')


async def authenticate_user(username: str, password: str) -> Optional[model.User]:
    """Authenticated user.

    Args:
        username (str): Username.
        password (str): Password.

    Returns:
        Optional[model.User]: User data.
    """
    user = await service.get_user_by_username(username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> model.User:
    """Get current user.

    Args:
        token (str, optional): Current token. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: Token is invalid.

    Returns:
        model.User: User data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message='Could not validate credentials',
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


__all__ = ('authenticate_user', 'get_current_user')
