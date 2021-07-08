from importlib import import_module

from pydantic import BaseSettings as PydanticBaseSettings

settings: PydanticBaseSettings


def create_config(config: str = 'development') -> PydanticBaseSettings:
    global settings
    try:
        _config = config.lower()
        Settings = import_module(f'core.config.{_config}').Settings
    except:
        Settings = import_module('core.config.development').Settings

    settings = Settings()
    return settings


__all__ = ('settings', 'create_config')
