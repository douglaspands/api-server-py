import os
from unittest.mock import patch

from apiserver.core import config


def test_create_config_default():
    settings_ = config.create_config()
    assert config.settings == settings_
    assert config.settings.POSTGRES_SERVER == 'localhost'
    assert config.settings.POSTGRES_USER == 'postgres'
    assert config.settings.POSTGRES_PASSWORD == 'docker'
    assert config.settings.POSTGRES_DB == 'apiserver'
    assert config.settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'


def test_create_config_development():
    settings_ = config.create_config('development')
    assert config.settings == settings_
    assert config.settings.POSTGRES_SERVER == 'localhost'
    assert config.settings.POSTGRES_USER == 'postgres'
    assert config.settings.POSTGRES_PASSWORD == 'docker'
    assert config.settings.POSTGRES_DB == 'apiserver'
    assert config.settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'


def test_create_config_production_1():
    env_dict = {
        'POSTGRES_SERVER': 'localhost',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'docker',
        'POSTGRES_DB': 'apiserver',
        'SECRET_KEY': '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    }
    with patch.dict(os.environ, env_dict, clear=True):
        settings_ = config.create_config('production')
        assert config.settings == settings_
        assert config.settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
        assert config.settings.POSTGRES_SERVER == 'localhost'
        assert config.settings.POSTGRES_USER == 'postgres'
        assert config.settings.POSTGRES_PASSWORD == 'docker'
        assert config.settings.POSTGRES_DB == 'apiserver'
        assert str(config.settings.SQLALCHEMY_DATABASE_URI) == 'postgresql://postgres:docker@localhost:5432/apiserver'


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
        settings_ = config.create_config('production')
        assert config.settings == settings_
        assert config.settings.SECRET_KEY == '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
        assert config.settings.POSTGRES_SERVER == 'localhost'
        assert config.settings.POSTGRES_USER == 'postgres'
        assert config.settings.POSTGRES_PASSWORD == 'docker'
        assert config.settings.POSTGRES_DB == 'apiserver'
        assert config.settings.SQLALCHEMY_DATABASE_URI == 'postgresql://xxxxxx:yyyyyy@localhost:5432/zzzzzzzz'


def test_create_config_config_not_found():
    env = 'xxxxxxxxxx'
    try:
        config.create_config(env)
        assert False

    except Exception as err:
        assert str(err) == f'Environment "{env}" not found!'
