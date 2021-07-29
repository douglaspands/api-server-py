from app.core.exceptions import generic


def test_base_error():
    try:
        raise generic.BaseError('Message error', '001')

    except generic.BaseError as err:
        assert repr(err) == "BaseError(code='001', message='Message error')"

    except Exception:
        assert False


def test_not_found_error():
    try:
        raise generic.NotFoundError('Message error', '001')

    except generic.NotFoundError as err:
        assert repr(err) == "NotFoundError(code='001', message='Message error')"

    except Exception:
        assert False


def test_business_logic_error():
    try:
        raise generic.BusinessLogicError('Message error', '001')

    except generic.BusinessLogicError as err:
        assert repr(err) == "BusinessLogicError(code='001', message='Message error')"

    except Exception:
        assert False
