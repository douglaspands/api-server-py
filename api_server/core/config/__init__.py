from importlib import import_module
import logging

from pydantic import BaseSettings as PydanticBaseSettings

logger = logging.getLogger(__name__)

settings: PydanticBaseSettings


def create_config(config_env: str = 'development') -> PydanticBaseSettings:
    global settings
    try:
        _module = config_env.lower()
        Settings = import_module(f'core.config.{_module}').Settings

    except Exception as err:
        logger.error(f'Environment "{config_env}" not found!')
        raise err

    settings = Settings()
    return settings


__all__ = ('settings', 'create_config')
