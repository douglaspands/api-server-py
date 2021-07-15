""" apiserver - Async to sync decorator
"""
import os
import asyncio
from typing import Any, Tuple, Callable, Coroutine

import nest_asyncio
from databases import Database
from sqlalchemy import MetaData

nest_asyncio.apply()


def get_alembic_config() -> Tuple[MetaData, str, Database]:
    """Get apiserver configurations for Alembic.

    Returns:
        Tuple[MetaData, str]: sqlalchemy.MetaData instance, sqlalchemy_url, databases.Database
    """
    from apiserver.main import create_app
    create_app(os.getenv('PYTHON_ENV', 'development'))

    from apiserver.core.config import settings
    from apiserver.core.databases.sqlalchemy import database, metadata

    return metadata, settings.SQLALCHEMY_DATABASE_URI, database


def use_db_async(func: Callable) -> Any:
    """Decorator for use database async.

    Args:
        func (Callable): Function async.

    Returns:
        Any: Return result of the function.
    """
    from apiserver.core.databases.sqlalchemy import database
    def wrapper(*args, **kwargs) -> Any:
        async def awrapper() -> Coroutine:
            async with database.transaction():
                res = await func(*args, **kwargs)
            return res
        return asyncio.run(awrapper())
    return wrapper


__all__ = ('get_alembic_config', 'async_database',)
