from datetime import timedelta

from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from apiserver.auth import services
from apiserver.core.config import settings
from apiserver.auth.schemas import TokenOut
from apiserver.auth.utils.token import create_access_token
from apiserver.core.exceptions.http import HTTPException

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/v1/token', response_model=TokenOut)
async def login_for_access_token(tokenIn: OAuth2PasswordRequestForm = Depends()) -> TokenOut:
    user = await services.authenticate_user(username=tokenIn.username, password=tokenIn.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message='Incorrect username or password',
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return TokenOut(access_token=access_token)


__all__ = ('router',)
