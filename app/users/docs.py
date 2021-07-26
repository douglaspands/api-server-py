
from typing import Any, Dict


list_users: Dict[str, Any] = {

    'name': 'List of users',
    'description': 'Get list of users.',
    'responses': {
        204: {'description': 'List of users empty.'}
    }
}

get_user: Dict[str, Any] = {
    'name': 'Get User',
    'description': 'Get user by ID.',
    'responses': {
        404: {'description': 'User not found.'}
    }
}

update_user: Dict[str, Any] = {
    'name': 'Update User',
    'description': 'Update user by ID.',
    'responses': {
        404: {'description': 'User not found.'}
    }
}

create_user: Dict[str, Any] = {
    'name': 'Create User',
    'description': 'Create user.',
}

delete_user: Dict[str, Any] = {
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
