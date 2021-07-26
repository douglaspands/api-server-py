from unittest.mock import MagicMock, patch

import pytest

from app.core.utils.eventloop import EventLoopThreadSafe


@pytest.mark.asyncio
async def test_event_loop_stop_error():
    MockThread = MagicMock
    with patch('app.core.utils.eventloop.threading.Thread', MockThread):
        event_loop = EventLoopThreadSafe()
        with pytest.raises(Exception) as excinfo:
            event_loop.stop()
        assert "Require call 'start' method before or was run." == str(excinfo.value)


@pytest.mark.asyncio
async def test_event_loop_run_error():
    MockThread = MagicMock
    with patch('app.core.utils.eventloop.threading.Thread', MockThread):
        event_loop = EventLoopThreadSafe()
        with pytest.raises(Exception) as excinfo:
            event_loop.run()
        assert "Cannot call directly! Begin EventLoopThreadSafe by start method." == str(excinfo.value)


@pytest.mark.asyncio
async def test_event_loop_run_coroutine_error():

    def function(*args, **kwargs):
        return True

    MockThread = MagicMock
    with patch('app.core.utils.eventloop.threading.Thread', MockThread):
        event_loop = EventLoopThreadSafe()
        with pytest.raises(Exception) as excinfo:
            event_loop.run_coroutine(function())
        assert "Require call 'start' method before or was run 'stop' method." == str(excinfo.value)


@pytest.mark.asyncio
async def test_event_loop_start_error():
    MockThread = MagicMock
    with patch('app.core.utils.eventloop.threading.Thread', MockThread):
        event_loop = EventLoopThreadSafe()
        event_loop.start()
        with pytest.raises(Exception) as excinfo:
            event_loop.start()
        assert "EventLoopThreadSafe active or was run 'stop' method." == str(excinfo.value)


@pytest.mark.asyncio
async def test_event_loop_ok():
    expect = {'message': 'async function test'}

    async def async_function(*args, **kwargs):
        return expect

    event_loop = EventLoopThreadSafe()
    event_loop.start()
    res = event_loop.run_coroutine(async_function())
    event_loop.stop()

    assert res == expect
