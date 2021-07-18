""" Asynchronous Database
"""
import asyncio
from typing import Any, Callable, Coroutine
import threading

from sqlalchemy import MetaData


class EventLoopThreadSafe(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self._was_started = threading.Event()
        self._was_stopped = threading.Event()
        self._loop = asyncio.new_event_loop()

    def start(self):
        if not self._was_started.is_set() and \
           not self._was_stopped.is_set():
            super().start()
        else:
            raise Exception("EventLoopThreadSafe active or was run 'stop' method.")

    def run(self):
        if not self._was_started.is_set() and \
           not self._was_stopped.is_set():
            self._was_started.set()
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        else:
            raise Exception("Cannot call directly!")

    def run_coroutine(self, coro: Coroutine) -> Any:
        if self._was_started.is_set() and \
           not self._was_stopped.is_set():
            future = asyncio.run_coroutine_threadsafe(coro, self._loop)
            return future.result()
        else:
            raise Exception("Require call 'start' method before or was run 'stop' method.")

    def stop(self):
        if self._was_started.is_set() and \
           not self._was_stopped.is_set():
            self._was_stopped.set()
            self._loop.call_soon_threadsafe(self._loop.stop)
        else:
            raise Exception("Require call 'start' method before or was run.")


class AsyncDatabase(EventLoopThreadSafe):

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


adb = AsyncDatabase()

__all__ = ('adb',)
