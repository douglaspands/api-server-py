from unittest.mock import MagicMock, patch

from sqlalchemy import MetaData

from app.core.utils.adba import AsyncDatabaseAdapter


def test_adba_metadata(settings):
    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.EventLoopThreadSafe', MagicMock):
            adba = AsyncDatabaseAdapter()
            assert isinstance(adba.metadata, MetaData)


def test_adba_sqlalchemy_url(settings):
    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.EventLoopThreadSafe', MagicMock):
            adba = AsyncDatabaseAdapter()
            assert adba.sqlalchemy_url == settings.SQLALCHEMY_DATABASE_URI


def test_adba_connect(settings):
    async def async_func():
        pass
    mm = MagicMock(async_func)
    mm.connect = async_func
    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.EventLoopThreadSafe', MagicMock):
            with patch('app.core.utils.adba.db', mm):
                adba = AsyncDatabaseAdapter()
                adba.connect()
                assert adba._has_connect


def test_adba_disconnect(settings):
    async def async_func():
        pass
    mm = MagicMock(async_func)
    mm.connect = async_func
    mm.disconnect = async_func
    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.EventLoopThreadSafe', MagicMock):
            with patch('app.core.utils.adba.db', mm):
                adba = AsyncDatabaseAdapter()
                adba.connect()
                assert adba._has_connect
                adba.disconnect()
                assert not adba._has_connect


def test_adba_decorator_noatomic_1(settings, async_magic_mock_class):
    expect_result = (True, 'Text', 1)

    async def async_func():
        pass

    mm = async_magic_mock_class()
    mm.connect = async_func
    mm.disconnect = async_func
    mm.transaction.return_value = async_magic_mock_class()

    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.db', mm):
            adba = AsyncDatabaseAdapter()

            @adba.async_migration()
            async def async_func():
                return expect_result

            adba.connect()
            assert adba._has_connect

            res = async_func()
            assert res == expect_result

            adba.disconnect()
            assert not adba._has_connect


def test_adba_decorator_noatomic_2(settings, async_magic_mock_class):
    expect_result = (True, 'Text', 1)

    async def async_func():
        pass

    mm = async_magic_mock_class()
    mm.connect = async_func
    mm.disconnect = async_func
    mm.transaction.return_value = async_magic_mock_class()

    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.db', mm):
            adba = AsyncDatabaseAdapter()

            @adba.async_migration(atomic=False)
            async def async_func():
                return expect_result

            adba.connect()
            assert adba._has_connect

            res = async_func()
            assert res == expect_result

            adba.disconnect()
            assert not adba._has_connect


def test_adba_decorator_atomic(settings, async_magic_mock_class):
    expect_result = (True, 'Text', 1)

    async def async_func():
        pass

    mm = async_magic_mock_class()
    mm.connect = async_func
    mm.disconnect = async_func
    mm.transaction.return_value = async_magic_mock_class()

    with patch('app.core.utils.adba.settings', settings):
        with patch('app.core.utils.adba.db', mm):
            adba = AsyncDatabaseAdapter()

            @adba.async_migration(atomic=True)
            async def async_func():
                return expect_result

            adba.connect()
            assert adba._has_connect

            res = async_func()
            assert res == expect_result

            adba.disconnect()
            assert not adba._has_connect
