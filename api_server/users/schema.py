from typing import Optional

from pydantic import EmailStr, SecretStr, validator
from core.schema import BaseSchema


class CreateUserIn(BaseSchema):
    email: EmailStr
    password_1: SecretStr
    password_2: SecretStr

    class Config:
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
        schema_extra = {
            'application/json': {
                'examples': {
                    'email': 'joao.silva@email.com',
                    'password1': '123456',
                    'password2': '123456',
                }
            }
        }

    @validator('password_2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password_1' in values and v != values['password_1']:
            raise ValueError('passwords do not match')
        return v


class UpdateUserIn(BaseSchema):
    email: EmailStr
    password_old: Optional[SecretStr]
    password_new_1: Optional[SecretStr]
    password_new_2: Optional[SecretStr]
    username: str
    active: bool

    class Config:
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
                'example': '123456'
            },
            'password_new_2': {
                'title': 'New second password',
                'description': 'New second password.',
                'example': '123456'
            },
            'username': {
                'title': 'Username',
                'description': 'Username.',
                'example': 'joao.silva'
            },
            'active': {
                'title': 'Active',
                'description': 'User is active.',
                'example': True
            },
        }
        schema_extra = {
            'application/json': {
                'examples': {
                    'email': 'joao.silva@email.com',
                    'password1': '123456',
                    'password2': '123456',
                    'username': 'joao.silva',
                    'active': True
                }
            }
        }

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('password_old')
    def old_password_fill(cls, v, values, **kwargs):
        if 'password_old' in values:
            raise ValueError('old password is required')
        return v

    @validator('password_new_1')
    def passwords_match_1(cls, v, values, **kwargs):
        if 'password_old' in values:
            raise ValueError('old password is required')
        if 'password_new_2' in values and v != values['password_new_2']:
            raise ValueError('passwords do not match')
        return v

    @validator('password_new_2')
    def passwords_match_2(cls, v, values, **kwargs):
        if 'password_new_1' in values and v != values['password_new_1']:
            raise ValueError('passwords do not match')
        return v


class UserOut(BaseSchema):
    id: int
    username: str
    email: str
    active: bool

    class Config:
        fields = {
            'id': {
                'title': 'User ID',
                'description': 'User ID.',
                'example': 1
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
            'active': {
                'title': 'Active',
                'description': 'User is active.',
                'example': True
            }
        }
        schema_extra = {
            'application/json': {
                'examples': {
                    'data': {
                        'id': 1,
                        'email': 'joao.silva@email.com',
                        'username': 'joao.silva',
                        'active': True
                    }
                },
            }
        }


__all__ = ('CreateUserIn', 'UpdateUserIn', 'UserOut')
