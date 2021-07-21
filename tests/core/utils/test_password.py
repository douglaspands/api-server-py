from apiserver.core.utils.password import verify_password, get_password_hash


def test_get_password_hash_ok():
    pass_input = 'TE123@456#st'
    res = get_password_hash(password=pass_input)
    assert isinstance(res, str)
    assert len(res) == 60


def test_get_password_hash_none():
    pass_input = None
    expect_res = "TypeError('secret must be unicode or bytes, not None')"
    try:
        get_password_hash(password=pass_input)
        assert False
    except TypeError as err:
        assert repr(err) == expect_res
    except Exception:
        assert False


def test_verify_password_true():
    pass_input = '123456'
    expect_res = True
    pass_hash = get_password_hash(password=pass_input)
    assert verify_password(plain_password=pass_input, hashed_password=pass_hash) == expect_res


def test_verify_password_false():
    pass_input = '123456'
    pass_input_2 = '654321'
    expect_res = False
    pass_hash = get_password_hash(password=pass_input)
    assert verify_password(plain_password=pass_input_2, hashed_password=pass_hash) == expect_res
