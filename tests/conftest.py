from unittest.mock import MagicMock

import pytest

from app.config import Settings


@pytest.fixture
def settings():
    args = {}
    args['POSTGRES_SERVER'] = 'localhost'
    args['POSTGRES_USER'] = 'scott'
    args['POSTGRES_PASSWORD'] = 'tiger'
    args['POSTGRES_DB'] = 'mydatabase'
    args['SECRET_KEY'] = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    args['ROUTERS'] = ['players:router_api', 'teams', 'flags:router']
    return Settings(**args)


@pytest.fixture
def async_magic_mock_class():
    class AsyncContextManagerMock(MagicMock):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for key in ('aenter_return', 'aexit_return'):
                setattr(self, key, kwargs[key] if key in kwargs else MagicMock())

        async def __aenter__(self):
            return self.aenter_return

        async def __aexit__(self, *args):
            return self.aexit_return

    return AsyncContextManagerMock


@pytest.fixture
async def mock_model(async_magic_mock_class):
    async def mock_delete(**kwargs):
        return True

    mockModel = async_magic_mock_class()
    mock_manager = async_magic_mock_class()

    async def mock_get(**kwargs):
        return mockModel

    mock_manager.get_or_none = mock_get
    mock_manager.delete = mock_delete
    mock_manager.save = mock_get
    mock_manager.update = mock_get
    mockModel.objects = mock_manager

    return mockModel
