from core.config.base import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = False


__all__ = ('Settings',)
