from apiserver.core.config.base import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = True
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'docker'
    POSTGRES_DB: str = 'apiserver'
    SECRET_KEY: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'


__all__ = ('Settings',)
