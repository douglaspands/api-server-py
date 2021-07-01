from datetime import timedelta

from auth import services
from fastapi import Depends, APIRouter, status
from core.config import settings
from auth.schemas import TokenOut
from auth.utils.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from core.exceptions.http import HTTPException

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/v1/token', response_model=TokenOut)
async def login_for_access_token(tokenIn: OAuth2PasswordRequestForm = Depends()):
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
    return {'access_token': access_token, 'token_type': 'bearer'}


__all__ = ('router',)
