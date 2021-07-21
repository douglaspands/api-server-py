from apiserver.core import schemas


def test_to_camel_ok():
    string = 'test_snake_case_to_camel_case'
    expect = 'testSnakeCaseToCamelCase'
    assert schemas.to_camel(string) == expect


def test_to_camel_error():
    string = None
    expect = Exception
    try:
        schemas.to_camel(string)
        assert False
    except expect as err:
        assert True


def test_baseschema():
    class User(schemas.BaseSchema):
        first_name: str
        last_name: str

    user = User(first_name='Peter', last_name='Quill').dict(by_alias=True)
    assert 'firstName' in user
    assert 'lastName' in user


def test_response_ok():
    class User(schemas.BaseSchema):
        first_name: str
        last_name: str

    res = schemas.ResponseOK(data=User(first_name='Peter', last_name='Quill').dict(by_alias=True)).dict(by_alias=True)
    assert 'data' in res
    assert 'firstName' in res['data']
    assert 'lastName' in res['data']
