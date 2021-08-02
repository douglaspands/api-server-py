from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth import controllers
from app.core import handlers
from app.users.models import User as UserModel
from app.core.exceptions.generic import BusinessLogicError

app = FastAPI()
handlers.init_app(app)
app.include_router(controllers.router)

client = TestClient(app)


def test_get_token_incorret_form(async_magic_mock_class, fix_params):

    async def async_func(*args, **kwargs):
        raise BusinessLogicError('Password do not match.')

    app.dependency_overrides = {}

    mock_service = async_magic_mock_class()
    mock_service.create_user = async_func

    app.dependency_overrides = {}
    mock_service = async_magic_mock_class()

    mock_service.authenticate_user = async_func

    with patch('app.auth.controllers.services', mock_service):

        payload = 'username=admin&password=admin'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = client.post('/auth/v1/token', params=fix_params, headers=headers, data=payload)

    assert response.status_code == 401
    assert response.json() == {'error': 'Incorrect username or password.'}


def test_get_token_ok(async_magic_mock_class, fix_params):

    async def async_func(*args, **kwargs):
        user1 = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )
        user1.id = 3
        return user1

    app.dependency_overrides = {}

    mock_service = async_magic_mock_class()
    mock_service.create_user = async_func

    app.dependency_overrides = {}
    mock_service = async_magic_mock_class()

    mock_service.authenticate_user = async_func

    with patch('app.auth.controllers.services', mock_service):

        payload = 'username=admin&password=admin'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = client.post('/auth/v1/token', params=fix_params, headers=headers, data=payload)

    assert response.status_code == 200

    res = response.json()

    assert res['token_type'] == 'bearer'
    assert isinstance(res['access_token'], str)
    assert len(res['access_token']) > 0
