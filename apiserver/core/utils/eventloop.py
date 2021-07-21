import asyncio
import threading
from typing import Any, Coroutine


class EventLoopThreadSafe(threading.Thread):

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self._was_started = threading.Event()
        self._was_stopped = threading.Event()
        self._loop = asyncio.new_event_loop()

    def run(self) -> None:
        if not self._was_started.is_set() and \
           not self._was_stopped.is_set():
            self._was_started.set()
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        else:
            raise Exception("Cannot call directly!")

    def start(self) -> None:
        if not self._was_started.is_set() and \
           not self._was_stopped.is_set():
            super().start()
        else:
            raise Exception("EventLoopThreadSafe active or was run 'stop' method.")

    def run_coroutine(self, coro: Coroutine) -> Any:
        if self._was_started.is_set() and \
           not self._was_stopped.is_set():
            future = asyncio.run_coroutine_threadsafe(coro, self._loop)
            return future.result()
        else:
            raise Exception("Require call 'start' method before or was run 'stop' method.")

    def stop(self) -> None:
        if self._was_started.is_set() and \
           not self._was_stopped.is_set():
            self._was_stopped.set()
            self._loop.call_soon_threadsafe(self._loop.stop)
        else:
            raise Exception("Require call 'start' method before or was run.")


__all__ = ('EventLoopThreadSafe',)
