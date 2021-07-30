from unittest.mock import patch

import pytest

from app.users.models import User as UserModel
from app.auth.middlewares import check_authentication
from app.auth.utils.token import create_access_token
from app.core.exceptions.http import HttpForbiddenError, HttpUnauthorizedError
from app.core.exceptions.generic import NotFoundError


@pytest.mark.asyncio
async def test_check_authentication_success_1(settings):

    async def mock_get_user(*args, **kwargs):
        user1 = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )
        user1.id = 6
        return user1

    with patch('app.auth.middlewares.settings', settings):

        with patch('app.auth.middlewares.user_service') as mock_service:

            mock_service.get_user = mock_get_user
            token_input = await create_access_token({'sub': 'unit.test'})
            user = await check_authentication(token_input)

    assert user.username == "jonh.roberts"
    assert user.is_active is True


@pytest.mark.asyncio
async def test_check_authentication_fail_1(settings):

    async def mock_get_user(*args, **kwargs):
        user1 = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=False
        )
        user1.id = 6
        return user1

    with patch('app.auth.middlewares.settings', settings):

        with patch('app.auth.middlewares.user_service') as mock_service:

            mock_service.get_user = mock_get_user
            token_input = await create_access_token({'sub': 'unit.test'})

            try:
                await check_authentication(token_input)

            except HttpForbiddenError as err:
                assert str(err) == 'Inactive user.'

            except BaseException:
                assert False


@pytest.mark.asyncio
async def test_check_authentication_fail_2(settings):

    async def mock_get_user(*args, **kwargs):
        raise NotFoundError('User not found.')

    with patch('app.auth.middlewares.settings', settings):

        with patch('app.auth.middlewares.user_service') as mock_service:

            mock_service.get_user = mock_get_user
            token_input = await create_access_token({'sub': 'unit.test'})

            try:
                await check_authentication(token_input)
                assert False

            except HttpUnauthorizedError as err:
                assert str(err) == 'Could not validate credentials.'

            except BaseException:
                assert False
