"""Users Services."""
from typing import Any, Dict, List, Union

from app.users.models import User as UserModel
from app.users.schemas import CreateUserIn, UpdateUserIn
from app.core.utils.password import verify_password, get_password_hash
from app.core.exceptions.generic import NotFoundError, BusinessLogicError


async def all_users(**kwargs: Any) -> List[UserModel]:
    """Get all users.

    Returns:
        List[UserModel]: List of user data.
    """
    return await UserModel.objects.all(**kwargs)


async def get_user(**kwargs: Any) -> UserModel:
    """Get first user by fields.

    Returns:
        UserModel: User data if exist.
    """
    user = await UserModel.objects.get_or_none(**kwargs)

    if not user:
        raise NotFoundError("User not found.")

    return user


async def create_user(user_input: Union[Dict[str, Any], CreateUserIn]) -> UserModel:
    """Create user.

    Args:
        user_input (Union[Dict[str, Any], CreateUserIn]): User data.

    Returns:
        UserModel: User created.
    """
    values = user_input.dict() if isinstance(user_input, CreateUserIn) else user_input
    values["username"] = values["email"].split("@")[0]
    values["password"] = get_password_hash(values["password_1"])
    values["is_active"] = True
    del values["password_1"]
    del values["password_2"]
    user = UserModel(**values)
    return await user.save()


async def update_user(id: int, user_input: Union[Dict[str, Any], UpdateUserIn]) -> UserModel:
    """Update user.

    Args:
        id (int): User ID.
        user_input (Union[Dict[str, Any], UpdateUserIn]): User data for update.

    Returns:
        UserModel: User updated.
    """
    user = await UserModel.objects.get_or_none(id=id)

    if not user:
        raise NotFoundError("User not found.")

    values = user_input.dict() if isinstance(user_input, UpdateUserIn) else user_input
    if values.get("password_old"):

        if not verify_password(values["password_old"], user.password):
            raise BusinessLogicError("Old password do not match.")

        values["password"] = get_password_hash(values["password_new_1"])
        del values["password_old"]
        del values["password_new_1"]
        del values["password_new_2"]

    for k, v in values.items():
        setattr(user, k, v)

    return await user.update()


async def delete_user(id: int) -> bool:
    """Delete user.

    Args:
        id (int): User ID.

    Returns:
        bool: True if remove successfully.
    """
    user = await UserModel.objects.get_or_none(id=id)

    if not user:
        raise NotFoundError("User not found.")

    await user.delete()
    return True
