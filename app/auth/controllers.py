"""Auth Controllers."""
from datetime import timedelta

from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import services
from app.config import settings
from app.auth.schemas import TokenOut
from app.auth.utils.token import create_access_token
from app.core.exceptions.http import HttpError

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/v1/token', response_model=TokenOut)
async def login_for_access_token(token_in: OAuth2PasswordRequestForm = Depends()) -> TokenOut:
    """Login by username and password.

    Args:
        token_in (OAuth2PasswordRequestForm, optional): User name and password. Defaults to Depends().

    Raises:
        HttpError: Unauthorize access.

    Returns:
        TokenOut: Bearer Token.
    """
    user = await services.authenticate_user(username=token_in.username, password=token_in.password)
    if not user:
        raise HttpError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message='Incorrect username or password',
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return TokenOut(access_token=access_token)


__all__ = ('router',)
