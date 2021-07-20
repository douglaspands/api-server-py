from importlib import reload
from unittest.mock import patch

from databases import Database
from sqlalchemy import MetaData


def test_module_ok():

    postgres_url = 'postgresql://scott:tiger@localhost:5432/mydatabase'

    class MockSetting:
        SQLALCHEMY_DATABASE_URI = postgres_url

    with patch('apiserver.core.config.settings', MockSetting) as mock:
        from apiserver.core.databases import sqlalchemy
        reload(sqlalchemy)

        assert isinstance(sqlalchemy.database, Database)
        assert isinstance(sqlalchemy.metadata, MetaData)
        assert sqlalchemy.database.url == postgres_url


def test_module_error():

    postgres_url = 'xxxxxxxxx'

    class MockSetting:
        SQLALCHEMY_DATABASE_URI = postgres_url

    with patch('apiserver.core.config.settings', MockSetting) as mock:
        mock.settings = MockSetting

        try:
            from apiserver.core.databases import sqlalchemy
            reload(sqlalchemy)
            assert False

        except BaseException:
            assert True
