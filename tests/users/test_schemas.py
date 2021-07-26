from app.users import schemas
from pydantic.error_wrappers import ValidationError


def test_password_invalid():
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


def test_password_valid():
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
