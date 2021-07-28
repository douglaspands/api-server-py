"""Users Controllers."""
from typing import Any, Dict, List

from fastapi import Depends, APIRouter, status

from app.users import docs, models, services
from app.core.schemas import ResponseOK
from app.users.schemas import UserOut, UserQuery, CreateUserIn, UpdateUserIn
from app.auth.middlewares import get_current_active_user
from app.core.exceptions.http import HttpError

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
    """Get list of users.

    Args:
        query (UserQuery, optional): Querystring filters. Defaults to Depends().
        current_user (models.User, optional): User data from token. Defaults to Depends(get_current_active_user).

    Raises:
        HttpError: Result empty.

    Returns:
        ResponseOK[List[UserOut]]: List of users.
    """
    users = await services.all_users(**query.dict(exclude_none=True))
    if users:
        return ResponseOK(data=users)
    else:
        raise HttpError(status_code=204)


@router.get('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **docs.get_user)
async def get_user(id: int,
                   current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    """Get user.

    Args:
        id (int): User ID.
        current_user (models.User, optional): User data from token. Defaults to Depends(get_current_active_user).

    Raises:
        HttpError: User not found.

    Returns:
        ResponseOK[UserOut]: User data.
    """
    user = await services.get_user(id=id)
    if user:
        return ResponseOK(data=user)
    else:
        raise HttpError(status_code=404)


@router.put('/v1/users/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ResponseOK[UserOut],
            **docs.update_user)
async def update_user(id: int,
                      user_input: UpdateUserIn,
                      current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    """Update user.

    Args:
        id (int): User ID.
        user_input (UpdateUserIn): User data update.
        current_user (models.User, optional): User data from token. Defaults to Depends(get_current_active_user).

    Raises:
        HttpError: user not found.

    Returns:
        ResponseOK[UserOut]: User data updated.
    """
    user = await services.update_user(id=id, user_input=user_input)
    if user:
        return ResponseOK(data=user)
    else:
        raise HttpError(status_code=404)


@router.post('/v1/users',
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseOK[UserOut],
             **docs.create_user)
async def create_user(user_input: CreateUserIn,
                      current_user: models.User = Depends(get_current_active_user)) -> ResponseOK[UserOut]:
    """Create user.

    Args:
        user_input (CreateUserIn): User data.
        current_user (models.User, optional): User data from token. Defaults to Depends(get_current_active_user).

    Returns:
        ResponseOK[UserOut]: User data created.
    """
    user = await services.create_user(user_input=user_input)
    return ResponseOK(data=user)


@router.delete('/v1/users/{id}',
               status_code=status.HTTP_200_OK,
               **docs.delete_user)
async def delete_user(id: int,
                      current_user: models.User = Depends(get_current_active_user)) -> Dict[str, Any]:
    """Remove user.

    Args:
        id (int): User ID.
        current_user (models.User, optional): User data from token. Defaults to Depends(get_current_active_user).

    Returns:
        Dict[str, Any]: Data empty.
    """
    await services.delete_user(id=id)
    return {}


__all__ = ('router',)
