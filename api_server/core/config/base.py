import secrets
from typing import Any, Dict, List, Optional

from pydantic import PostgresDsn
from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import validator


class BaseSettings(PydanticBaseSettings):

    SERVER_TITLE: str = 'API Manager'
    SERVER_VERSION: str = '1.0.0'
    SERVER_DESCRIPTION: str = 'OpenAPI schema'

    API_PREFIX: str = '/api'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    AUTH_TOKEN_URL: str = '/auth/v1/token'

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    ROUTERS: List[str] = [
        'auth.controllers',
        'users.controllers'
    ]

    class Config:
        case_sensitive = True


__all__ = ('BaseSettings',)
