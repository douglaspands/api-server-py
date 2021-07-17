from apiserver.core.exceptions.http import HTTPException


def test_http_exception_raise():
    try:
        raise HTTPException(status_code=500, message='Generic Erro')

    except HTTPException as err:
        assert err.status_code == 500
        assert err.error == 'Generic Erro'
    
    except Exception:
        assert False


def test_http_exception_repr():
    try:
        raise HTTPException(status_code=500, message='Generic Erro')

    except HTTPException as err:
        assert repr(err) == "HTTPException(status_code=500, error='Generic Erro')"
    
    except Exception:
        assert False