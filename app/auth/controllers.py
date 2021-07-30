"""Auth Controllers."""
from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import docs, services
from app.config import settings
from app.auth.schemas import TokenOut
from app.auth.utils.token import create_access_token
from app.core.exceptions.http import HttpUnauthorizedError

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/v1/token', response_model=TokenOut, **docs.get_token)
async def get_token(token_in: OAuth2PasswordRequestForm = Depends()) -> TokenOut:
    """Get token for system access.

    Args:
        token_in (OAuth2PasswordRequestForm, optional): User data. Defaults to Depends().

    Raises:
        HttpUnauthorizedError: Unauthorized access.

    Returns:
        TokenOut: Bearer Token.
    """
    user = await services.authenticate_user(username=token_in.username, password=token_in.password)
    if not user:
        raise HttpUnauthorizedError(message='Incorrect username or password')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return TokenOut(access_token=access_token)


__all__ = ('router',)
