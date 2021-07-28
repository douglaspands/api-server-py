"""Configurations."""
from __future__ import annotations

import os
import secrets
from typing import Any, Dict, List, Union, Optional

from pydantic import PostgresDsn, BaseSettings, validator


class Settings(BaseSettings):
    """Global Settings."""

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
    SQLALCHEMY_DATABASE_URI: Optional[Union[PostgresDsn, str]] = None

    AUTH_TOKEN_URL: str = '/auth/v1/token'

    @validator('SQLALCHEMY_DATABASE_URI', pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """PostgreSQL Url.

        Args:
            v (Optional[str]): Value received.
            values (Dict[str, Any]): Others values.

        Returns:
            Any: Return url connection.
        """
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
        """Metadata."""

        case_sensitive = True

    @classmethod
    def from_env(cls) -> Settings:
        """Configure settings by environment."""
        env = os.getenv('PYTHON_ENV', 'development')
        env_fields: Dict[str, Any] = {}

        if env.upper() in ('DEVELOPMENT', 'PRODUCTION'):

            if env.upper() == 'DEVELOPMENT':
                env_fields['POSTGRES_SERVER'] = 'localhost'
                env_fields['POSTGRES_USER'] = 'postgres'
                env_fields['POSTGRES_PASSWORD'] = 'docker'
                env_fields['POSTGRES_DB'] = 'apiserver'
                env_fields['SECRET_KEY'] = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'

        else:
            raise Exception(f'Environment "{env}" not found!')

        return cls(**env_fields)


settings = Settings.from_env()

__all__ = ('settings', 'Settings')
