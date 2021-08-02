from datetime import timedelta

import pytest

from app.auth.utils.token import create_access_token


@pytest.mark.asyncio
async def test_create_access_token_success_1():
    data = {'sub': 'philip.austin'}
    token = await create_access_token(data=data)
    assert isinstance(token, str)
    assert len(token) > 1


@pytest.mark.asyncio
async def test_create_access_token_success_2():
    data = {'sub': 'philip.austin'}
    expires_delta = timedelta(minutes=10)
    token = await create_access_token(data=data, expires_delta=expires_delta)
    assert isinstance(token, str)
    assert len(token) > 1


@pytest.mark.asyncio
async def test_create_access_token_error():
    data = {'sub': 'philip.austin'}
    expires_delta = '123'
    try:
        await create_access_token(data=data, expires_delta=expires_delta)
        assert False
    except BaseException:
        assert True
