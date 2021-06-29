import secrets
from typing import Any, Dict, List, Optional

from pydantic import PostgresDsn, BaseSettings, validator


class Settings(BaseSettings):

    API_PREFIX: str = '/api'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str
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
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    ROUTERS: List[str] = [
        'auth.controller',
        'users.controller'
    ]

    class Config:
        case_sensitive = True
        env_file = '../local.env'
        env_file_encoding = 'utf-8'


settings = Settings()


__all__ = ('settings',)
