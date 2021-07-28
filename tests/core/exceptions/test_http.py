from app.core.exceptions.http import HttpError


def test_http_exception_raise():
    try:
        raise HttpError(status_code=500, message='Generic Erro')

    except HttpError as err:
        assert err.status_code == 500
        assert err.error == 'Generic Erro'
    
    except Exception:
        assert False


def test_http_exception_repr():
    try:
        raise HttpError(status_code=500, message='Generic Erro')

    except HttpError as err:
        assert repr(err) == "HttpError(status_code=500, error='Generic Erro')"
    
    except Exception:
        assert False