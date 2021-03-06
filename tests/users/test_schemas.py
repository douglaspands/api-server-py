from pydantic.error_wrappers import ValidationError

from app.users import schemas


def test_createuserin_password_invalid():
    user = {
        "email": "joao.silva@email.com",
        "password1": "123456",
        "password2": "654321"
    }
    expect_msg = "1 validation error for CreateUserIn\npassword2\n  passwords do not match (type=value_error)"
    try:
        schemas.CreateUserIn(**user)
        assert False
    except ValidationError as err:
        assert str(err) == expect_msg
    except BaseException:
        assert False


def test_createuserin_valid():
    user = {
        "email": "joao.silva@email.com",
        "password1": "123456",
        "password2": "123456"
    }
    try:
        schemas.CreateUserIn(**user)
        assert True
    except BaseException:
        assert False


def test_updateuserin_username_invalid():
    user = {
        "username": "&¨&¨&¨(A¨*S&AHJHKJ",
        "email": "joao.silva@email.com",
        "is_active": True
    }
    expect_msg = "1 validation error for UpdateUserIn\nusername\n  must be alphanumeric (type=value_error)"
    try:
        schemas.UpdateUserIn(**user)
        assert False
    except ValidationError as err:
        assert str(err) == expect_msg
    except BaseException:
        assert False


def test_updateuserin_password_old_required():
    user = {
        "username": "joao.silva",
        "email": "joao.silva@email.com",
        "password_new_1": "123456",
        "is_active": True
    }
    expect_msg = "1 validation error for UpdateUserIn\npasswordNew1\n  old password is required (type=value_error)"
    try:
        schemas.UpdateUserIn(**user)
        assert False
    except ValidationError as err:
        assert str(err) == expect_msg
    except BaseException:
        assert False


def test_updateuserin_passwords_nomatch():
    user = {
        "username": "joao.silva",
        "email": "joao.silva@email.com",
        "password_old": "xxxxxxx",
        "password_new_1": "123456",
        "password_new_2": "654321",
        "is_active": True
    }
    expect_msg = "1 validation error for UpdateUserIn\npasswordNew2\n  passwords do not match (type=value_error)"
    try:
        schemas.UpdateUserIn(**user)
        assert False
    except ValidationError as err:
        assert str(err) == expect_msg
    except BaseException:
        assert False


def test_updateuserin_valid():
    user = {
        "username": "joao.silva",
        "email": "joao.silva@email.com",
        "password_old": "xxxxxxx",
        "password_new_1": "123456",
        "password_new_2": "123456",
        "is_active": True
    }
    try:
        schemas.UpdateUserIn(**user)
        assert True
    except BaseException:
        assert False


def test_userout_valid():
    user_out = schemas.UserOut(
        id=1,
        username='unit.test',
        email='unit.test@email.com',
        is_active=True
    )
    assert user_out.id == 1
    assert user_out.email == 'unit.test@email.com'
    assert user_out.username == 'unit.test'
    assert user_out.is_active is True
    assert user_out.dict(by_alias=True) == {
        'id': 1,
        'email': 'unit.test@email.com',
        'username': 'unit.test',
        'isActive': True
    }
