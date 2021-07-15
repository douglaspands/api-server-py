""" apiserver - Async to sync decorator
"""
import os
import asyncio
from typing import Any, Tuple, Callable, Coroutine

from sqlalchemy import MetaData


def get_alembic_config() -> Tuple[MetaData, str]:
    """Get apiserver configurations for Alembic.

    Returns:
        Tuple[MetaData, str]: sqlalchemy.MetaData instance, sqlalchemy_url
    """
    from apiserver.main import create_app
    create_app(os.getenv('PYTHON_ENV', 'development'))

    from apiserver.core.config import settings
    from apiserver.core.databases.sqlalchemy import metadata

    return metadata, settings.SQLALCHEMY_DATABASE_URI


def use_db_async(func: Callable) -> Any:
    """Decorator for use database async.

    Args:
        func (Callable): Function async.

    Returns:
        Any: Return result of the function.
    """
    from apiserver.main import create_app
    create_app(os.getenv('PYTHON_ENV', 'development'))
    def wrapper(*args, **kwargs) -> Any:
        async def wrapper_async() -> Coroutine:
            from apiserver.core.databases.sqlalchemy import database
            res = None
            error = None
            try:
                await database.connect()
                res = await func(*args, **kwargs)
            except Exception as err:
                error = err
            finally:
                await database.disconnect()
            if error:
                raise error
            return res
        return asyncio.run(wrapper_async())
    return wrapper


__all__ = ('get_alembic_config', 'async_database',)
