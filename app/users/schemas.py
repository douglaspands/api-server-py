import re
from typing import Any, Optional

from pydantic import EmailStr, validator
from pydantic.main import BaseModel
from fastapi.param_functions import Query

from app.core.schemas import BaseConfig, BaseSchema


class CreateUserIn(BaseSchema):
    email: EmailStr
    password_1: str
    password_2: str

    class Config(BaseConfig):
        fields = {
            'email': {
                'title': 'Email',
                'description': 'Email.',
                'example': 'joao.silva@email.com'
            },
            'password_1': {
                'title': 'First password',
                'description': 'First password.',
                'example': '123456'
            },
            'password_2': {
                'title': 'Second password',
                'description': 'Second password.',
                'example': '123456'
            }
        }

    @validator('password_2')
    def passwords_match(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        if 'password_1' not in values or v != values['password_1']:
            raise ValueError('passwords do not match')
        return v


class UpdateUserIn(BaseSchema):
    email: EmailStr
    password_old: Optional[str]
    password_new_1: Optional[str]
    password_new_2: Optional[str]
    username: str
    is_active: bool

    class Config(BaseConfig):
        fields = {
            'email': {
                'title': 'Email',
                'description': 'Email.',
                'example': 'joao.silva@email.com'
            },
            'password_old': {
                'title': 'Old password',
                'description': 'Old password.',
                'example': '123456'
            },
            'password_new_1': {
                'title': 'New first password',
                'description': 'New first password.',
                'example': '654321'
            },
            'password_new_2': {
                'title': 'New second password',
                'description': 'New second password (Need to be the same as the passwordNew1).',
                'example': '654321'
            },
            'username': {
                'title': 'Username',
                'description': 'Username.',
                'example': 'joao.silva'
            },
            'is_active': {
                'title': 'Active',
                'description': 'User is active.',
                'example': True
            },
        }

    @validator('username')
    def username_valid(cls, v: Any) -> Any:
        if not re.search(r'^[a-zA-Z0-9._]+$', v):
            raise ValueError('must be alphanumeric')
        return v

    @validator('password_new_1')
    def passwords_match_1(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        if 'password_old' not in values:
            raise ValueError('old password is required')
        return v

    @validator('password_new_2')
    def passwords_match_2(cls, v: Any, values: Any, **kwargs: Any) -> Any:
        if 'password_new_1' not in values or v != values['password_new_1']:
            raise ValueError('passwords do not match')
        return v


class UserOut(BaseSchema):
    id: int
    username: str
    email: str
    is_active: bool

    class Config(BaseConfig):
        fields = {
            'id': {
                'title': 'User ID',
                'description': 'User ID.',
                'example': 2
            },
            'email': {
                'title': 'Email',
                'description': 'Email.',
                'example': 'joao.silva@email.com'
            },
            'username': {
                'title': 'Username',
                'description': 'Username.',
                'example': 'joao.silva'
            },
            'is_active': {
                'title': 'Active',
                'description': 'User is active.',
                'example': True
            }
        }


class UserQuery(BaseModel):
    is_active: Optional[bool] = Query(None,
                                      title='Ask if is active users',
                                      description='List of the active users.')


__all__ = ('CreateUserIn', 'UpdateUserIn', 'UserOut', 'UserQuery')
