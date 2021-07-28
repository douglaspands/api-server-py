"""Core Password Utils."""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Generate password hash.

    Args:
        password (str): Raw password.

    Returns:
        str: Password hash.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify matched password.

    Args:
        plain_password (str): Password raw.
        hashed_password (str): Password hash.

    Returns:
        bool: Same password is True.
    """
    return pwd_context.verify(plain_password, hashed_password)


__all__ = ('get_password_hash', 'verify_password')
