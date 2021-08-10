"""Core Async Database Adapter."""
from typing import Any, Union, Callable, Optional

from pydantic import PostgresDsn
from sqlalchemy import MetaData
from databases.core import Transaction
from fastapi.applications import FastAPI

from app.config import settings
from app.core.utils.eventloop import EventLoopThreadSafe
from app.core.databases.sqlalchemy import database as db
from app.core.databases.sqlalchemy import metadata as md


class AsyncDatabaseAdapter(EventLoopThreadSafe):
    """Async database adapter for sync functions."""

    def __init__(self, app: Optional[FastAPI] = None) -> None:
        super().__init__()
        self.start()
        self._app = app
        self._database = db
        self._has_connect = False

    @property
    def metadata(self) -> MetaData:
        """Get metadata for domains models.

        Returns:
            MetaData: Database metadata.
        """
        return md

    @property
    def sqlalchemy_url(self) -> Optional[Union[str, PostgresDsn]]:
        """SQLAlchemy URL from database.

        Returns:
            Optional[Union[str, PostgresDsn]]: URL from database.
        """
        return settings.SQLALCHEMY_DATABASE_URI

    def connect(self) -> None:
        """Async database connect for sync functions."""

        async def wrapper() -> None:
            """Wrapper sync to async database connect."""
            await self._database.connect()

        if self._has_connect is False:
            self.run_coroutine(wrapper())
            self._has_connect = True

    def disconnect(self) -> None:
        """Async database disconnect for sync functions."""

        async def wrapper() -> None:
            """Wrapper sync to async database disconnect."""
            await self._database.disconnect()

        if self._has_connect is True:
            self.run_coroutine(wrapper())
            self._has_connect = False
        self.stop()

    def async_migration(self, atomic: bool = False) -> Callable:
        """Async database use decorator on sync functions.

        Args:
            atomic (bool, optional): Run function with transaction context. Defaults to False.

        Returns:
            Callable: Function run with decorator context.
        """

        def decorator(func: Callable) -> Callable:
            """Run function.

            Args:
                func (Callable): Function to be run.

            Returns:
                Callable: Function run with decorator context.
            """

            def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
                """Decorator async to sync function."""

                async def awrapper() -> Optional[Any]:
                    """Wrapper run async function."""
                    if atomic is True:
                        async with self.transaction():
                            res = await func(*args, **kwargs)
                    else:
                        res = await func(*args, **kwargs)
                    return res

                return self.run_coroutine(awrapper())

            wrapper.__name__ = func.__name__
            return wrapper

        return decorator

    def transaction(self) -> Transaction:
        """Transaction context."""
        return self._database.transaction()


__all__ = ("AsyncDatabaseAdapter",)
