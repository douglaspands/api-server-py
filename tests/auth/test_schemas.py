from app.auth import schemas


def test_tokenout_valid_1():
    token_out = schemas.TokenOut(
        access_token='1234567890',
    )
    assert token_out.access_token == '1234567890'
    assert token_out.token_type == 'bearer'
    assert token_out.dict(by_alias=True) == {
        'access_token': '1234567890',
        'token_type': 'bearer'
    }


def test_tokenout_valid_2():
    token_out = schemas.TokenOut(
        access_token='0987654321',
        token_type='teste'
    )
    assert token_out.access_token == '0987654321'
    assert token_out.token_type == 'teste'
    assert token_out.dict(by_alias=True) == {
        'access_token': '0987654321',
        'token_type': 'teste'
    }
