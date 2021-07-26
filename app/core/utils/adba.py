from typing import Any, Callable, Optional, Union

from pydantic import PostgresDsn
from sqlalchemy import MetaData
from fastapi.applications import FastAPI

from app.config import settings
from app.core.utils.eventloop import EventLoopThreadSafe
from app.core.databases.sqlalchemy import database as db
from app.core.databases.sqlalchemy import metadata as md


class AsyncDatabaseByApp(EventLoopThreadSafe):

    def __init__(self, app: Optional[FastAPI] = None) -> None:
        super().__init__()
        self.start()
        self._app = app
        self._database = db
        self._has_connect = False

    @property
    def metadata(self) -> MetaData:
        return md

    @property
    def sqlalchemy_url(self) -> Optional[Union[str, PostgresDsn]]:
        return settings.SQLALCHEMY_DATABASE_URI

    def connect(self) -> None:
        async def wrapper() -> None:
            await self._database.connect()
        if self._has_connect is False:
            self.run_coroutine(wrapper())
            self._has_connect = True

    def disconnect(self) -> None:
        async def wrapper() -> None:
            await self._database.disconnect()
        if self._has_connect is True:
            self.run_coroutine(wrapper())
            self._has_connect = False
        self.stop()

    def async_migration(self, func: Callable) -> Callable:
        """Asynchronous migration decorator.
        """
        def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
            async def awrapper() -> Optional[Any]:
                async with self._database.transaction():
                    res = await func(*args, **kwargs)
                return res
            return self.run_coroutine(awrapper())
        wrapper.__name__ = func.__name__
        return wrapper


__all__ = ('AsyncDatabaseByApp',)
