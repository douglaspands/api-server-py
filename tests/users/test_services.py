from datetime import datetime

from fastapi.exceptions import HTTPException
from app.users import services
from unittest.mock import patch
import pytest
from app.users.models import User as UserModel


@pytest.mark.asyncio
async def test_allusers_with_content(async_magic_mock_class):
    async def mock_all(*args, **kwargs):
        return [UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )]

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.all = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        users = await services.all_users()
        assert len(users) == 1
        assert users[0].email == "jonh.roberts@email.com"
        assert users[0].password == "123456"
        assert users[0].username == "jonh.roberts"
        assert users[0].is_active
        assert isinstance(users[0].created_at, datetime)
        assert isinstance(users[0].updated_at, datetime)


@pytest.mark.asyncio
async def test_allusers_no_content(async_magic_mock_class):
    async def mock_all(*args, **kwargs):
        return []

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.all = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        users = await services.all_users()
        assert len(users) == 0


@pytest.mark.asyncio
async def test_get_user_by_id_with_content(async_magic_mock_class):
    async def mock_all(**kwargs):
        pk = kwargs.get('id')
        user = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )
        user.id = pk
        return user

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        user = await services.get_user(id=2)
        assert user.id == 2
        assert user.email == "jonh.roberts@email.com"
        assert user.password == "123456"
        assert user.username == "jonh.roberts"
        assert user.is_active
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_user_by_id_no_content(async_magic_mock_class):
    async def mock_all(**kwargs):
        return None

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        user = await services.get_user(id=3)
        assert user is None


@pytest.mark.asyncio
async def test_get_user_by_username_with_content(async_magic_mock_class):
    async def mock_all(**kwargs):
        username = kwargs.get('username')
        user = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username=username,
            is_active=True
        )
        user.id = 2
        return user

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        username = 'jonh.roberts'
        user = await services.get_user(username=username)
        assert user.id == 2
        assert user.email == "jonh.roberts@email.com"
        assert user.password == "123456"
        assert user.username == username
        assert user.is_active
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_user_by_username_no_content(async_magic_mock_class):
    async def mock_all(**kwargs):
        return None

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        user = await services.get_user(username="xpto.xpto")
        assert user is None


@pytest.mark.asyncio
async def test_delete_user_ok(mock_model):
    async def mock_delete(**kwargs):
        return True

    mockUserModel = mock_model

    with patch('app.users.services.UserModel', mockUserModel):
        res = await services.delete_user(id=2)
        assert res is True


@pytest.mark.asyncio
async def test_delete_user_nok(async_magic_mock_class):
    async def mock_all(**kwargs):
        return None

    mockUserModel = async_magic_mock_class()
    mockUserModel.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mockUserModel):
        try:
            await services.delete_user(id=2)
            assert False
        except HTTPException as err:
            assert err.detail == 'User not found'
        except BaseException:
            assert False
