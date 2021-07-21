from typing import Optional
from importlib import import_module

from pydantic import BaseSettings as PydanticBaseSettings

settings: Optional[PydanticBaseSettings] = None


def create_config(config_env: str = 'development') -> Optional[PydanticBaseSettings]:
    global settings
    try:
        _module_name = config_env.lower()
        _module = import_module(f'apiserver.core.config.{_module_name}')

    except BaseException:
        raise Exception(f'Environment "{config_env}" not found!')

    settings = _module.Settings()  # type: ignore

    return settings


__all__ = ('settings', 'create_config')
