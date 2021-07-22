from unittest import mock

from fastapi import FastAPI

from apiserver.core import routers


def test_init_app(settings):
    app = FastAPI()
    with mock.patch('apiserver.core.routers.settings', settings):
        routers.init_app(app)
        assert hasattr(app, 'routes')
