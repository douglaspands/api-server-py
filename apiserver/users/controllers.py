from typing import Any, Dict, List

from fastapi import Depends, APIRouter, status

from apiserver.users import docs, models, services
from apiserver.core.schemas import ResponseOK
from apiserver.users.schemas import UserOut, UserQuery, CreateUserIn, UpdateUserIn
from apiserver.auth.middlewares import get_current_active_user
from apiserver.core.exceptions.http import HTTPException

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/v1/users',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[List[UserOut]],
            **docs.list_users)
async def list_users(query: UserQuery = Depends(),
                     current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[List[UserOut]]:
    users = await services.all_users(**query.dict(exclude_none=True))
    if users:
        return ResponseOK(data=users)
    else:
        raise HTTPException(status_code=204)


@router.get('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **docs.get_user)
async def get_user(id: int,
                   current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    user = await services.get_user_by_id(id=id)
    if user:
        return ResponseOK(data=user)
    else:
        raise HTTPException(status_code=404)


@router.put('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **docs.update_user)
async def update_user(id: int,
                      user_input: UpdateUserIn,
                      current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    user = await services.update_user(id=id, user_input=user_input)
    if user:
        return ResponseOK(data=user)
    else:
        raise HTTPException(status_code=404)


@router.post('/v1/users',
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseOK[UserOut],
             **docs.create_user)
async def create_user(user_input: CreateUserIn,
                      current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    user = await services.create_user(user_input=user_input)
    return ResponseOK(data=user)


@router.delete('/v1/users/{id}',
               status_code=status.HTTP_200_OK,
               **docs.delete_user)
async def delete_user(id: int,
                      current_user: models.User = Depends(get_current_active_user)) -> Dict[str, Any]:
    await services.delete_user(id=id)
    return {}


__all__ = ('router',)
