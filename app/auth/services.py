"""Auth Services."""
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.users import services
from app.config import settings
from app.users.models import User as UserModel
from app.core.utils.password import verify_password
from app.core.exceptions.http import HttpUnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}{settings.AUTH_TOKEN_URL}')


async def authenticate_user(username: str, password: str) -> Optional[UserModel]:
    """Authenticater user.

    Args:
        username (str): Username.
        password (str): Password.

    Returns:
        Optional[UserModel]: User data.
    """
    try:
        user = await services.get_user(username=username)
        if verify_password(password, user.password):
            return user

    except BaseException:
        pass

    finally:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """Get current user.

    Args:
        token (str, optional): Current token. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: Token is invalid.

    Returns:
        UserModel: User data.
    """
    credentials_exception = HttpUnauthorizedError('Could not validate credentials')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            raise credentials_exception

        user = await services.get_user(username=username)
        return user

    except JWTError:
        raise credentials_exception

    except BaseException:
        return None


__all__ = ('authenticate_user', 'get_current_user')
