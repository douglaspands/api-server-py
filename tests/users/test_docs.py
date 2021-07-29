from app.users import docs


def test_list_users():
    assert docs.list_users == {
        'name': 'List of users',
        'description': 'Get list of users.',
        'responses': {
            204: {'description': 'List of users empty.'},
            401: {'description': 'Unathorized token.'},
            403: {'description': 'Forbidden token.'},
        }
    }


def test_get_user():
    assert docs.get_user == {
        'name': 'Get User',
        'description': 'Get user by ID.',
        'responses': {
            401: {'description': 'Unathorized token.'},
            403: {'description': 'Forbidden token.'},
            404: {'description': 'User not found.'}
        }
    }


def test_update_user():
    assert docs.update_user == {
        'name': 'Update User',
        'description': 'Update user by ID.',
        'responses': {
            401: {'description': 'Unathorized token.'},
            403: {'description': 'Forbidden token.'},
            404: {'description': 'User not found.'},
            422: {
                'title': 'UnprocessableEntity.',
                'description': 'Business logic error.',
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': '#/components/schemas/HTTPUnprocessableEntity'
                        },
                        'examples': {
                            'password_not_matched': {
                                'value': {
                                    'error': 'Old password do not match.'
                                }
                            }
                        },
                    }
                }
            }
        }
    }


def test_create_user():
    assert docs.create_user == {
        'name': 'Create User',
        'description': 'Create user.',
        'responses': {
            401: {'description': 'Unathorized token.'},
            403: {'description': 'Forbidden token.'},
        }
    }


def test_delete_user():
    assert docs.delete_user == {
        'name': 'Delete User',
        'description': 'Delete user.',
        'responses': {
            401: {'description': 'Unathorized token.'},
            403: {'description': 'Forbidden token.'},
            404: {'description': 'User not found.'}
        }
    }
