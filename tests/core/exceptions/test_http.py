from app.core.exceptions import http


def test_http_exception_raise():
    try:
        raise http.HttpError(status_code=500, message='Generic Erro')

    except http.HttpError as err:
        assert err.status_code == 500
        assert err.error == 'Generic Erro'

    except Exception:
        assert False


def test_http_exception_repr():
    try:
        raise http.HttpError(status_code=500, message='Generic Erro')

    except http.HttpError as err:
        assert repr(err) == "HttpError(status_code=500, error='Generic Erro')"

    except Exception:
        assert False


def test_http_not_content():
    try:
        raise http.HttpNoContentError()

    except http.HttpNoContentError as err:
        assert repr(err) == "HttpNoContentError(status_code=204, error='')"

    except Exception:
        assert False


def test_http_unauthorized():
    try:
        raise http.HttpUnauthorizedError('No permission.')

    except http.HttpUnauthorizedError as err:
        assert repr(err) == "HttpUnauthorizedError(status_code=401, error='No permission.')"

    except Exception:
        assert False


def test_http_forbidden():
    try:
        raise http.HttpForbiddenError('No permission.')

    except http.HttpForbiddenError as err:
        assert repr(err) == "HttpForbiddenError(status_code=403, error='No permission.')"

    except Exception:
        assert False


def test_http_not_found():
    try:
        raise http.HttpNotFoundError()

    except http.HttpNotFoundError as err:
        assert repr(err) == "HttpNotFoundError(status_code=404, error='')"

    except Exception:
        assert False


def test_http_unprocessable():
    try:
        raise http.HttpUnprocessableEntityError('Business error')

    except http.HttpUnprocessableEntityError as err:
        assert repr(err) == "HttpUnprocessableEntityError(status_code=422, error='Business error')"

    except Exception:
        assert False
