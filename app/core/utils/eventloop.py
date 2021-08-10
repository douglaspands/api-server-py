"""Core Event Loop Thread Safe."""
import asyncio
import threading
from typing import Any, Coroutine


class EventLoopThreadSafe(threading.Thread):
    """Create event loop thread safe."""

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self._was_started = threading.Event()
        self._was_stopped = threading.Event()

    def start(self) -> None:
        """Start event loop."""
        if not self._was_started.is_set() and not self._was_stopped.is_set():
            self._was_started.set()
            self._loop = asyncio.new_event_loop()
            super().start()
        else:
            raise Exception("EventLoopThreadSafe active or was run 'stop' method.")

    def run(self) -> None:
        """Run event loop forever."""
        if self._was_started.is_set() and not self._was_stopped.is_set():
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        else:
            raise Exception("Cannot call directly! Begin EventLoopThreadSafe by start method.")

    def run_coroutine(self, coro: Coroutine) -> Any:
        """Run coroutine inside sync function.

        Args:
            coro (Coroutine): Coroutine.

        Raises:
            Exception: Error caused by running method  before start method.

        Returns:
            Any: Result of the coroutine.
        """
        if self._was_started.is_set() and not self._was_stopped.is_set():
            future = asyncio.run_coroutine_threadsafe(coro=coro, loop=self._loop)
            return future.result()
        else:
            raise Exception("Require call 'start' method before or was run 'stop' method.")

    def stop(self) -> None:
        """Stop event loop."""
        if self._was_started.is_set() and not self._was_stopped.is_set():
            self._was_stopped.set()
            self._loop.call_soon_threadsafe(self._loop.stop)
        else:
            raise Exception("Require call 'start' method before or was run.")


__all__ = ("EventLoopThreadSafe",)
