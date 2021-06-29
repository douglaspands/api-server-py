
list_users = {
    'name': 'List of users',
    'description': 'Get list of users.',
    'responses': {
        204: {'description': 'List of users empty.'}
    }
}

get_user = {
    'name': 'Get User',
    'description': 'Get user by ID.',
    'responses': {
        404: {'description': 'User not found.'}
    }
}

update_user = {
    'name': 'Update User',
    'description': 'Update user by ID.',
    'responses': {
        404: {'description': 'User not found.'}
    }
}

create_user = {
    'name': 'Create User',
    'description': 'Create user.',
}

delete_user = {
    'name': 'Delete User',
    'description': 'Delete user.',
    'responses': {
        404: {'description': 'User not found.'}
    }
}


__all__ = (
    'list_users',
    'get_user',
    'update_user',
    'create_user',
    'delete_user',
)
