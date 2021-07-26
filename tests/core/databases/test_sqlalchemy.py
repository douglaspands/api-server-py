from importlib import import_module, reload
from unittest import mock

from databases import Database
from sqlalchemy import MetaData


def test_module_ok(settings):

    expect_url = str(settings.SQLALCHEMY_DATABASE_URI).replace('tiger', '********')

    with mock.patch('app.config.settings', settings):
        sqlalchemy = import_module('app.core.databases.sqlalchemy')
        reload(sqlalchemy)
        assert isinstance(sqlalchemy.database, Database)
        assert isinstance(sqlalchemy.metadata, MetaData)
        database_url = repr(sqlalchemy.database.url).replace("DatabaseURL('", "").replace("')", "")
        assert database_url == expect_url


def test_module_error(settings):

    settings.SQLALCHEMY_DATABASE_URI = 'xxxxxxxxx'

    with mock.patch('app.config.settings', settings):
        try:
            sqlalchemy = import_module('app.core.databases.sqlalchemy')
            reload(sqlalchemy)
            assert False
        except BaseException:
            assert True
