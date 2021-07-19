from typing import Any, Callable, Coroutine

from sqlalchemy import MetaData

from apiserver.core.utils.event_loop import EventLoopThreadSafe


class AsyncDatabaseFromAppCreated(EventLoopThreadSafe):

    def __init__(self):
        super().__init__()
        self.start()
        from apiserver.main import create_app
        self._app = create_app()
        from apiserver.core.databases.sqlalchemy import database
        self._database = database
        self._has_connect = False

    @property
    def metadata(self) -> MetaData:
        from apiserver.core.databases.sqlalchemy import metadata
        return metadata

    @property
    def sqlalchemy_url(self) -> str:
        from apiserver.core.config import settings
        return settings.SQLALCHEMY_DATABASE_URI

    def connect(self):
        async def wrapper():
            await self._database.connect()
        if self._has_connect is False:
            self.run_coroutine(wrapper())
            self._has_connect = True

    def disconnect(self):
        async def wrapper():
            await self._database.disconnect()
        if self._has_connect is True:
            self.run_coroutine(wrapper())
            self._has_connect = False
        self.stop()

    def async_migration(self, func: Callable) -> Any:
        """Asynchronous migration decorator.
        """
        def wrapper(*args, **kwargs) -> Any:
            async def awrapper() -> Coroutine:
                async with self._database.transaction():
                    res = await func(*args, **kwargs)
                return res
            return self.run_coroutine(awrapper())
        wrapper.__name__ = func.__name__
        return wrapper


__all__ = ('AsyncDatabaseFromAppCreated',)
