from importlib import import_module

from pydantic import BaseSettings as PydanticBaseSettings

settings: PydanticBaseSettings = None


def create_config(config_env: str = 'development') -> PydanticBaseSettings:
    global settings
    try:
        _module = config_env.lower()
        Settings = import_module(f'apiserver.core.config.{_module}').Settings

    except BaseException:
        raise Exception(f'Environment "{config_env}" not found!')

    settings = Settings()
    return settings


__all__ = ('settings', 'create_config')
