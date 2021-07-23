import os
from unittest.mock import patch

from apiserver.core.config import Settings


def test_create_config_default():
    settings = Settings.from_env()
    assert settings.POSTGRES_SERVER == 'localhost'
    assert settings.POSTGRES_USER == 'postgres'
    assert settings.POSTGRES_PASSWORD == 'docker'
    assert settings.POSTGRES_DB == 'apiserver'
    assert settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'


def test_create_config_development():
    os.environ['PYTHON_ENV'] = 'development'
    settings = Settings.from_env()
    assert settings.POSTGRES_SERVER == 'localhost'
    assert settings.POSTGRES_USER == 'postgres'
    assert settings.POSTGRES_PASSWORD == 'docker'
    assert settings.POSTGRES_DB == 'apiserver'
    assert settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'


def test_create_config_production_1():
    env_dict = {
        'POSTGRES_SERVER': 'localhost',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'docker',
        'POSTGRES_DB': 'apiserver',
        'SECRET_KEY': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    }
    with patch.dict(os.environ, env_dict, clear=True):
        os.environ['PYTHON_ENV'] = 'production'
        settings = Settings.from_env()
        assert settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
        assert settings.POSTGRES_SERVER == 'localhost'
        assert settings.POSTGRES_USER == 'postgres'
        assert settings.POSTGRES_PASSWORD == 'docker'
        assert settings.POSTGRES_DB == 'apiserver'
        assert str(settings.SQLALCHEMY_DATABASE_URI) == 'postgresql://postgres:docker@localhost:5432/apiserver'


def test_create_config_production_2():
    env_dict = {
        'POSTGRES_SERVER': 'localhost',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'docker',
        'POSTGRES_DB': 'apiserver',
        'SECRET_KEY': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
        'SQLALCHEMY_DATABASE_URI': 'postgresql://xxxxxx:yyyyyy@localhost:5432/zzzzzzzz'
    }
    with patch.dict(os.environ, env_dict, clear=True):
        os.environ['PYTHON_ENV'] = 'production'
        settings = Settings.from_env()
        assert settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
        assert settings.POSTGRES_SERVER == 'localhost'
        assert settings.POSTGRES_USER == 'postgres'
        assert settings.POSTGRES_PASSWORD == 'docker'
        assert settings.POSTGRES_DB == 'apiserver'
        assert settings.SQLALCHEMY_DATABASE_URI == 'postgresql://xxxxxx:yyyyyy@localhost:5432/zzzzzzzz'


def test_create_config_config_not_found():
    env = 'xxxxxxxxxx'
    os.environ['PYTHON_ENV'] = env
    try:
        Settings.from_env()
        assert False

    except Exception as err:
        assert str(err) == f'Environment "{env}" not found!'
