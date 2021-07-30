from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core import handlers
from app.users import controllers
from app.users.models import User as UserModel
from app.users.controllers import check_authentication
from app.core.exceptions.generic import NotFoundError, BusinessLogicError

app = FastAPI()
handlers.init_app(app)
app.include_router(controllers.router)

client = TestClient(app)


def test_list_users_unauthorized(async_magic_mock_class):

    async def async_func(*args, **kwargs):
        return []

    app.dependency_overrides = {}
    mock_service = async_magic_mock_class()

    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.get('/users/v1/users')

    assert response.status_code == 401


def test_list_users_empty(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        return []

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.get('/users/v1/users', params=fix_params)

        assert response.status_code == 204
        assert response.json() is None


def test_list_users_query_valid_1(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        assert kwargs['is_active'] is True
        return []

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        fix_params.update({'is_active': True})
        response = client.get('/users/v1/users', params=fix_params)

        assert response.status_code == 204
        assert response.json() is None


def test_list_users_query_valid_2(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        assert kwargs['is_active'] is False
        return []

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        fix_params.update({'is_active': False})
        response = client.get('/users/v1/users', params=fix_params)

        assert response.status_code == 204
        assert response.json() is None


def test_list_users_query_invalid(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        assert kwargs.get('test') is None
        return []

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        fix_params.update({'test': False})
        response = client.get('/users/v1/users', params=fix_params)

        assert response.status_code == 204
        assert response.json() is None


def test_list_users_ok(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        user1 = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )
        user1.id = 2
        user2 = UserModel(
            email="philipe.roberts@email.com",
            password="123456",
            username="philipe.roberts",
            is_active=True
        )
        user2.id = 3
        return [user1, user2]

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.all_users = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.get('/users/v1/users', params=fix_params)

        assert response.status_code == 200
        assert response.json() == {
            "data": [
                {
                    "id": 2,
                    "email": "jonh.roberts@email.com",
                    "username": "jonh.roberts",
                    "isActive": True
                },
                {
                    "id": 3,
                    "email": "philipe.roberts@email.com",
                    "username": "philipe.roberts",
                    "isActive": True
                }
            ]
        }


def test_create_user_ok(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        user_input = kwargs.get('user_input')
        user1 = UserModel(
            email=user_input.email,
            password=user_input.password_1,
            username=user_input.email.split('@')[0],
            is_active=True
        )
        user1.id = 4
        return user1

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.create_user = async_func

    with patch('app.users.controllers.services', mock_service):

        payload = {
            "email": "abcd.efgh@email.com",
            "password1": "123456",
            "password2": "123456",
        }
        expect_response = payload.copy()
        expect_response['id'] = 4
        expect_response['username'] = payload['email'].split('@')[0]
        expect_response['isActive'] = True
        del expect_response['password1']
        del expect_response['password2']

        response = client.post('/users/v1/users', params=fix_params, json=payload)

        assert response.status_code == 201
        assert response.json() == {"data": expect_response}


def test_delete_user_ok(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        return True

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.delete_user = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.delete('/users/v1/users/6', params=fix_params)

        assert response.status_code == 200
        assert response.json() == {}


def test_delete_user_not_found(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        raise NotFoundError('User not found.')

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.delete_user = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.delete('/users/v1/users/6', params=fix_params)

        assert response.status_code == 404


def test_get_user_ok(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        assert kwargs.get('id') == 6
        user1 = UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )
        user1.id = kwargs['id']
        return user1

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.get_user = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.get('/users/v1/users/6', params=fix_params)

        assert response.status_code == 200
        assert response.json() == {
            'data': {
                "id": 6,
                "email": "jonh.roberts@email.com",
                "username": "jonh.roberts",
                "isActive": True
            }
        }


def test_get_user_not_found(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        assert kwargs.get('id') == 7
        raise NotFoundError('User not found.')

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.get_user = async_func

    with patch('app.users.controllers.services', mock_service):

        response = client.get('/users/v1/users/7', params=fix_params)

        assert response.status_code == 404


def test_update_user_ok(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        user_id = kwargs.get('id')
        user_input = kwargs.get('user_input')
        user1 = UserModel(
            email=user_input.email,
            password='*****',
            username=user_input.username,
            is_active=True
        )
        user1.id = user_id
        return user1

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.update_user = async_func

    with patch('app.users.controllers.services', mock_service):

        user_id = 4

        payload = {
            "username": "abcd.efgh",
            "email": "abcd.efgh@email.com",
            "isActive": True
        }
        expect_response = payload.copy()
        expect_response['id'] = user_id
        expect_response['username'] = payload['username']
        expect_response['isActive'] = True

        response = client.put(f'/users/v1/users/{user_id}', params=fix_params, json=payload)

        assert response.status_code == 200
        assert response.json() == {"data": expect_response}


def test_update_user_business_error(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        raise BusinessLogicError('Password not matched.')

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.update_user = async_func

    with patch('app.users.controllers.services', mock_service):

        user_id = 4

        payload = {
            "username": "abcd.efgh",
            "email": "abcd.efgh@email.com",
            "isActive": True,
            "passwordOld": "123456",
            "passwordNew1": "654321",
            "passwordNew2": "654321",
        }

        response = client.put(f'/users/v1/users/{user_id}', params=fix_params, json=payload)

        assert response.status_code == 422
        assert response.json() == {"error": "Password not matched."}


def test_update_user_not_found(async_magic_mock_class, mock_current_active_user, fix_params):

    async def async_func(*args, **kwargs):
        raise NotFoundError('User not found.')

    app.dependency_overrides = {}
    app.dependency_overrides[check_authentication] = mock_current_active_user

    mock_service = async_magic_mock_class()
    mock_service.update_user = async_func

    with patch('app.users.controllers.services', mock_service):

        user_id = 4

        payload = {
            "username": "abcd.efgh",
            "email": "abcd.efgh@email.com",
            "isActive": True,
            "passwordOld": "123456",
            "passwordNew1": "654321",
            "passwordNew2": "654321",
        }

        response = client.put(f'/users/v1/users/{user_id}', params=fix_params, json=payload)

        assert response.status_code == 404
