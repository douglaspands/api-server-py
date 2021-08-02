from datetime import datetime
from unittest.mock import patch

import pytest

from app.auth import services
from app.users.models import User as UserModel
from app.core.exceptions.generic import NotFoundError, BusinessLogicError


@pytest.mark.asyncio
async def test_authenticate_user_ok(async_magic_mock_class):
    async def mock_srv_func(*args, **kwargs):
        user = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True)
        user.id = 2
        return user

    mock_service = async_magic_mock_class()
    mock_service.get_user = mock_srv_func

    with patch('app.auth.services.user_service', mock_service):
        with patch('app.auth.services.verify_password', return_value=True):
            user = await services.authenticate_user(username="jonh.roberts", password="123456")
            assert user.email == "jonh.roberts@email.com"
            assert user.password == "123456"
            assert user.username == "jonh.roberts"
            assert user.is_active
            assert isinstance(user.created_at, datetime)
            assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_authenticate_user_notfound(async_magic_mock_class):
    async def mock_srv_func(*args, **kwargs):
        raise NotFoundError('User not found!')

    mock_service = async_magic_mock_class()
    mock_service.get_user = mock_srv_func

    with patch('app.auth.services.user_service', mock_service):
        try:
            await services.authenticate_user(username="jonh.roberts", password="123456")
            assert False
        except NotFoundError as err:
            assert str(err) == 'User not found!'
        except BaseException:
            assert False


@pytest.mark.asyncio
async def test_authenticate_user_password_not_matched(async_magic_mock_class):
    async def mock_srv_func(*args, **kwargs):
        user = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True)
        user.id = 2
        return user

    mock_service = async_magic_mock_class()
    mock_service.get_user = mock_srv_func

    with patch('app.auth.services.user_service', mock_service):
        with patch('app.auth.services.verify_password', return_value=False):
            try:
                await services.authenticate_user(username="jonh.roberts", password="123456")
                assert False
            except BusinessLogicError as err:
                assert str(err) == 'Password do not match.'
            except BaseException:
                assert False
