from typing import Any, Dict, List, Union, Optional
from datetime import datetime

import pydantic
from users import model, schema
from fastapi.exceptions import HTTPException
from core.utils.password import get_password_hash, verify_password


async def all_users(**kwargs) -> List[model.User]:
    """Get all users.

    Returns:
        List[model.User]: List of user data.
    """
    return await model.User.objects.all(**kwargs)


async def get_user_by_id(id: int) -> Optional[model.User]:
    """Get user by ID.

    Args:
        id (int): User ID.

    Returns:
        Optional[model.User]: User data if exist.
    """
    return await model.User.objects.get_or_none(id=id)


async def get_user_by_username(username: str) -> Optional[model.User]:
    """Get user by username.

    Args:
        username (str): User username.

    Returns:
        Optional[model.User]: User data if exist.
    """
    return await model.User.objects.get_or_none(username=username)


async def get_user(id: int) -> Optional[model.User]:
    """Get user by ID.

    Args:
        id (int): User ID.

    Returns:
        Optional[model.User]: User data if exist.
    """
    return await model.User.objects.get_or_none(id=id)

async def create_user(user_input: Union[Dict[str, Any], schema.CreateUserIn]) -> model.User:
    """Create user.

    Args:
        user_input (Union[Dict[str, Any], schema.UserIn]): User data.
    Returns:
        model.User: User created.
    """
    values = user_input.dict() if isinstance(user_input, pydantic.BaseModel) else user_input
    values['username'] = values['email'].split('@')[0]
    values['password'] = get_password_hash(values['password_1'])
    values['active'] = True
    del values['password_1']
    del values['password_2']
    user = model.User(**values)
    return await user.save()


async def update_user(id: int, user_input: Union[Dict[str, Any], schema.UpdateUserIn]) -> Optional[model.User]:
    """Update user.

    Args:
        id (int): User ID.
        user_input (Union[Dict[str, Any], schema.UserIn]): User data for update.

    Returns:
        Optional[model.User]: User updated.
    """
    user = await model.User.objects.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    values = user_input.dict() if isinstance(user_input, pydantic.BaseModel) else user_input
    if values.get('password_old'):
        if verify_password(values['password_old'], user.password):
            raise HTTPException(status_code=422, detail='Old password do not match')
        values['password'] = get_password_hash(values['password_new_1'])
        del values['password_old']
        del values['password_new_1']
        del values['password_new_2']
    for k, v in values.items():
        setattr(user, k, v)
    user.updated_at = datetime.utcnow()
    return await user.update()


async def delete_user(id: int) -> bool:
    """Delete user.

    Args:
        id (int): User ID.

    Returns:
        bool: True if remove successfully.
    """
    user = await model.User.objects.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    await user.objects.delete()
    return True
