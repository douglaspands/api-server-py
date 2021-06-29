from typing import List

from core.schema import ResponseOK
from fastapi import APIRouter, status, Depends

from users import doc
from users.schema import CreateUserIn, UpdateUserIn, UserOut
from users import service
from auth.middleware import get_current_active_user
from users import model
from core.exception.http import HTTPException


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/v1/users',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[List[UserOut]],
            **doc.list_users)
async def list_users(current_user: model.User = Depends(get_current_active_user)):
    users = await service.all_users()
    if users:
        return ResponseOK(data=users)
    else:
        raise HTTPException(status_code=204, message='No content')


@router.get('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **doc.get_user)
async def get_user(id: int, current_user: model.User = Depends(get_current_active_user)):
    user = await service.get_user_by_id(id=id)
    if user:
        return ResponseOK(data=user)
    else:
        raise HTTPException(status_code=404, message='User not found')


@router.put('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **doc.update_user)
async def update_user(id: int, user_input: UpdateUserIn, current_user: model.User = Depends(get_current_active_user)):
    user = await service.update_user(id=id, user_input=user_input)
    if user:
        return ResponseOK(data=user)
    else:
        raise HTTPException(status_code=404, message='User not found')


@router.post('/v1/users',
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseOK[UserOut],
             **doc.create_user)
async def create_user(user_input: CreateUserIn):
    user = await service.create_user(user_input=user_input)
    return ResponseOK(data=user)


@router.delete('/v1/users/{id}',
               status_code=status.HTTP_200_OK,
               **doc.delete_user)
async def delete_user(id: int, current_user: model.User = Depends(get_current_active_user)):
    await service.delete_user(id=id)
    return {}


__all__ = ('router',)
