from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI

from app import api


def test_create_app_instante(settings):
    with patch('app.api.settings', settings):
        with patch('app.api.openapi', MagicMock()):
            with patch('app.api.routers', MagicMock()):
                with patch('app.api.handlers', MagicMock()):
                    app = api.create_app()
                    assert isinstance(app, FastAPI)


@pytest.mark.asyncio
async def test_startup_event_ok(settings, async_magic_mock_class):

    AsyncContextManagerMock = async_magic_mock_class
    connection_result = {'ok': False}

    async def mock_connection():
        connection_result['ok'] = True

    mock_database = AsyncContextManagerMock()
    mock_database.connect = mock_connection

    with patch('app.api.settings', settings):
        with patch('app.api.openapi', MagicMock()):
            with patch('app.api.routers', MagicMock()):
                with patch('app.api.handlers', MagicMock()):
                    with patch('app.api.database', mock_database):
                        app = api.create_app()

                        await app.router.startup()
                        assert connection_result.get('ok', False)


@pytest.mark.asyncio
async def test_shutdown_event_ok(settings, async_magic_mock_class):

    AsyncContextManagerMock = async_magic_mock_class
    connection_result = {'ok': False}

    async def mock_connection():
        connection_result['ok'] = True

    mock_database = AsyncContextManagerMock()
    mock_database.disconnect = mock_connection

    with patch('app.api.settings', settings):
        with patch('app.api.openapi', MagicMock()):
            with patch('app.api.routers', MagicMock()):
                with patch('app.api.handlers', MagicMock()):
                    with patch('app.api.database', mock_database):
                        app = api.create_app()

                        await app.router.shutdown()
                        assert connection_result.get('ok', False)
