"""Auth Services."""
from app.users import services as user_service
from app.users.models import User as UserModel
from app.core.utils.password import verify_password
from app.core.exceptions.generic import BusinessLogicError


async def authenticate_user(username: str, password: str) -> UserModel:
    """Authenticater user.

    Args:
        username (str): Username.
        password (str): Password.

    Returns:
        UserModel: User data.
    """
    user = await user_service.get_user(username=username)
    if not verify_password(password, user.password):
        raise BusinessLogicError('Password do not match.')
    return user


__all__ = ('authenticate_user',)
