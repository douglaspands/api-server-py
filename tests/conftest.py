import pytest

from apiserver.core import config


@pytest.fixture
def settings():
    args = {}
    args['POSTGRES_SERVER'] = 'localhost'
    args['POSTGRES_USER'] = 'scott'
    args['POSTGRES_PASSWORD'] = 'tiger'
    args['POSTGRES_DB'] = 'mydatabase'
    args['SECRET_KEY'] = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    args['ROUTERS'] = ['players:router_api', 'teams', 'flags:router']
    return config.Settings(**args)
