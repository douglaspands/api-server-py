from app.users import docs


def test_get_docs():
    assert docs.list_users == {
        'name': 'List of users',
        'description': 'Get list of users.',
        'responses': {
            204: {'description': 'List of users empty.'}
        }
    }

    assert docs.get_user == {
        'name': 'Get User',
        'description': 'Get user by ID.',
        'responses': {
            404: {'description': 'User not found.'}
        }
    }

    assert docs.update_user == {
        'name': 'Update User',
        'description': 'Update user by ID.',
        'responses': {
            404: {'description': 'User not found.'}
        }
    }

    assert docs.create_user == {
        'name': 'Create User',
        'description': 'Create user.',
    }

    assert docs.delete_user == {
        'name': 'Delete User',
        'description': 'Delete user.',
        'responses': {
            404: {'description': 'User not found.'}
        }
    }
