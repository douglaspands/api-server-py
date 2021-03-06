from datetime import datetime
from unittest.mock import patch

import pytest

from app.users import services
from app.users.models import User as UserModel
from app.users.schemas import CreateUserIn, UpdateUserIn
from app.core.exceptions.generic import NotFoundError, BusinessLogicError


@pytest.mark.asyncio
async def test_allusers_with_content(async_magic_mock_class):
    async def mock_all(*args, **kwargs):
        return [UserModel(
            email="jonh.roberts@email.com",
            password="123456",
            username="jonh.roberts",
            is_active=True
        )]

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.all = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
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

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.all = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
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

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
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

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
        try:
            await services.get_user(id=3)
            assert False
        except NotFoundError:
            assert True
        except BaseException:
            assert False


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

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
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

    mock_user_model = async_magic_mock_class()
    mock_user_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_user_model):
        try:
            await services.get_user(username="xpto.xpto")
            assert False
        except NotFoundError:
            assert True
        except BaseException:
            assert False


@pytest.mark.asyncio
async def test_delete_user_ok(async_magic_mock_class):

    async def mock_delete(**kwargs):
        return True

    async def mock_all(**kwargs):
        mock_model = async_magic_mock_class()
        mock_model.delete = mock_delete
        return mock_model

    mock_model = async_magic_mock_class()
    mock_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_model):
        res = await services.delete_user(id=2)
        assert res is True


@pytest.mark.asyncio
async def test_delete_user_nok(async_magic_mock_class):
    async def mock_all(**kwargs):
        return None

    mock_model = async_magic_mock_class()
    mock_model.objects.get_or_none = mock_all

    with patch('app.users.services.UserModel', mock_model):
        try:
            await services.delete_user(id=2)
            assert False
        except NotFoundError as err:
            assert str(err) == 'User not found.'
        except BaseException:
            assert False


@pytest.mark.asyncio
async def test_create_user_ok_1(async_magic_mock_class):

    async def mock_save(self, *args, **kwargs):
        user = UserModel(
            email=self.email,
            password=self.password,
            username=self.username,
            is_active=self.is_active
        )
        user.id = 2
        return user

    user_input = {
        "email": "jonh.roberts@email.com",
        "password_1": "123456",
        "password_2": "123456",
    }

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        mock_model.save = mock_save
        user = await services.create_user(user_input)
        assert user.id == 2
        assert user.email == user_input["email"]
        assert len(user.password) > 0
        assert user.username == user_input["email"].split("@")[0]
        assert user.is_active is True


@pytest.mark.asyncio
async def test_create_user_ok_2(async_magic_mock_class):

    async def mock_save(self, *args, **kwargs):
        user = UserModel(
            email=self.email,
            password=self.password,
            username=self.username,
            is_active=self.is_active
        )
        user.id = 2
        return user

    user_input = {
        "email": "jonh.roberts@email.com",
        "password_1": "123456",
        "password_2": "123456",
    }
    user_input_schema = CreateUserIn(**user_input)

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        mock_model.save = mock_save
        user = await services.create_user(user_input_schema)
        assert user.id == 2
        assert user.email == user_input["email"]
        assert len(user.password) > 0
        assert user.username == user_input["email"].split("@")[0]
        assert user.is_active is True


@pytest.mark.asyncio
async def test_update_user_pass_invalid(async_magic_mock_class):

    async def mock_update(self, *args, **kwargs):
        return self

    async def mock_get_or_none(*args, **kwargs):
        user = UserModel(
            email="jonh.roberts@email.com",
            password="654321",
            username="jonh.roberts",
            is_active=True
        )
        user.id = kwargs.get('id')
        user.update = mock_update
        return user

    user_id = 2
    user_input = {
        "email": "jonh.roberts@email.com",
        "username": "jonh123456",
        "password_old": "654321",
        "password_new_1": "123456",
        "password_new_2": "123456",
    }

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        with patch('app.users.services.verify_password', return_value=False):
            mock_model.objects = async_magic_mock_class()
            mock_model.objects.get_or_none = mock_get_or_none
            try:
                await services.update_user(user_id, user_input)
                assert False
            except BusinessLogicError as err:
                assert str(err) == 'Old password do not match.'
            except BaseException:
                assert False


@pytest.mark.asyncio
async def test_update_user_not_found(async_magic_mock_class):

    async def mock_get_or_none(*args, **kwargs):
        return None

    user_id = 2
    user_input = {
        "email": "jonh.roberts@email.com",
        "username": "jonh123456",
        "password_old": "654321",
        "password_new_1": "123456",
        "password_new_2": "123456",
    }

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        mock_model.objects = async_magic_mock_class()
        mock_model.objects.get_or_none = mock_get_or_none
        try:
            await services.update_user(user_id, user_input)
            assert False
        except NotFoundError as err:
            assert str(err) == 'User not found.'
        except BaseException:
            assert False


@pytest.mark.asyncio
async def test_update_user_ok_1(async_magic_mock_class):

    def mock_update(model):
        _model = model

        async def awrapper(*args, **kwargs):
            return _model

        return awrapper

    async def mock_get_or_none(*args, **kwargs):
        user = UserModel(
            email="jonh.roberts@email.com",
            password="654321",
            username="jonh.roberts",
            is_active=True
        )
        user.id = kwargs.get('id')
        user.update = mock_update(user)
        return user

    user_id = 2
    user_input = {
        "email": "jonh.roberts@email.com",
        "username": "jonh123456",
        "password_old": "654321",
        "password_new_1": "123456",
        "password_new_2": "123456",
        "is_active": True
    }

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        with patch('app.users.services.verify_password', return_value=True):
            mock_model.objects = async_magic_mock_class()
            mock_model.objects.get_or_none = mock_get_or_none
            user = await services.update_user(user_id, user_input)
            assert user.id == user_id
            assert user.email == user_input["email"]
            assert len(user.password) > 0
            assert user.username == user_input["username"]
            assert user.is_active is True


@pytest.mark.asyncio
async def test_update_user_ok_2(async_magic_mock_class):

    def mock_update(model):
        _model = model

        async def awrapper(*args, **kwargs):
            return _model

        return awrapper

    async def mock_get_or_none(*args, **kwargs):
        user = UserModel(
            email="jonh.roberts@email.com",
            password="654321",
            username="jonh.roberts",
            is_active=True
        )
        user.id = kwargs.get('id')
        user.update = mock_update(user)
        return user

    user_id = 2
    user_input = {
        "email": "jonh.roberts@email.com",
        "username": "jonh123456",
        "password_old": "654321",
        "password_new_1": "123456",
        "password_new_2": "123456",
        "is_active": True
    }
    user_input_schema = UpdateUserIn(**user_input)

    with patch('app.users.services.UserModel', async_magic_mock_class) as mock_model:
        with patch('app.users.services.verify_password', return_value=True):
            mock_model.objects = async_magic_mock_class()
            mock_model.objects.get_or_none = mock_get_or_none
            user = await services.update_user(user_id, user_input_schema)
            assert user.id == user_id
            assert user.email == user_input["email"]
            assert len(user.password) > 0
            assert user.username == user_input["username"]
            assert user.is_active is True
