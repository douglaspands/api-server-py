"""Users Schemas."""
import re
from typing import Any, Optional

from pydantic import EmailStr, validator

from app.core.schemas import BaseConfig, BaseSchema


class CreateUserIn(BaseSchema):
    """User create schema."""

    email: EmailStr
    password_1: str
    password_2: str

    class Config(BaseConfig):
        """metadata."""

        fields = {
            "email": {"title": "Email", "description": "Email.", "example": "joao.silva@email.com"},
            "password_1": {"title": "First password", "description": "First password.", "example": "123456"},
            "password_2": {"title": "Second password", "description": "Second password.", "example": "123456"},
        }

    @validator("password_2")
    def passwords_match(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        """Password match validator.

        Args:
            v (Any): Value of the password.
            values (Any): Others attributes.

        Raises:
            ValueError: Passowrd do not match.

        Returns:
            Any: Password valid.
        """
        if "password_1" not in values or v != values["password_1"]:
            raise ValueError("passwords do not match")
        return v


class UpdateUserIn(BaseSchema):
    """User update schema."""

    email: EmailStr
    password_old: Optional[str]
    password_new_1: Optional[str]
    password_new_2: Optional[str]
    username: str
    is_active: bool

    class Config(BaseConfig):
        """Metadata."""

        fields = {
            "email": {"title": "Email", "description": "Email.", "example": "joao.silva@email.com"},
            "password_old": {"title": "Old password", "description": "Old password.", "example": "123456"},
            "password_new_1": {
                "title": "New first password",
                "description": "New first password.",
                "example": "654321",
            },
            "password_new_2": {
                "title": "New second password",
                "description": "New second password (Need to be the same as the passwordNew1).",
                "example": "654321",
            },
            "username": {"title": "Username", "description": "Username.", "example": "joao_silva_2"},
            "is_active": {"title": "Active", "description": "User is active.", "example": True},
        }

    @validator("username")
    def username_valid(cls, v: Any) -> Any:
        """Username validator.

        Args:
            v (Any): Username value.

        Raises:
            ValueError: Username invalid.

        Returns:
            Any: Username valid.
        """
        if not re.search(r"^[a-zA-Z0-9._]+$", v):
            raise ValueError("must be alphanumeric")
        return v

    @validator("password_new_1")
    def passwords_match_1(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        """Check if filled password_new_1 and password_old.

        Args:
            v (Any): Password value.
            values (Any): Others attributes.

        Raises:
            ValueError: Password invalid.

        Returns:
            Any: Password valid.
        """
        if not values.get("password_old"):
            raise ValueError("old password is required")
        return v

    @validator("password_new_2")
    def passwords_match_2(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        """Check if is same password_new_1 and password_new_2.

        Args:
            v (Any): Password value.
            values (Any): Others attributes.

        Raises:
            ValueError: Password invalid.

        Returns:
            Any: Password valid.
        """
        if not values.get("password_new_1") or v != values["password_new_1"]:
            raise ValueError("passwords do not match")
        return v


class UserOut(BaseSchema):
    """User response schema."""

    id: int
    username: str
    email: str
    is_active: bool

    class Config(BaseConfig):
        """Metadata."""

        fields = {
            "id": {"title": "User ID", "description": "User ID.", "example": 2},
            "email": {"title": "Email", "description": "Email.", "example": "joao.silva@email.com"},
            "username": {"title": "Username", "description": "Username.", "example": "joao.silva"},
            "is_active": {"title": "Active", "description": "User is active.", "example": True},
        }


__all__ = (
    "CreateUserIn",
    "UpdateUserIn",
    "UserOut",
)
