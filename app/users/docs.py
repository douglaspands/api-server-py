"""Users OpenApiDocs."""
from typing import Any, Dict

base_responses = {
    401: {"description": "Unathorized token."},
    403: {"description": "Forbidden token."},
}

response_422 = {
    "title": "UnprocessableEntity.",
    "description": "Business logic error.",
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/HTTPUnprocessableEntity"},
            "examples": {"password_not_matched": {"value": {"error": "Old password do not match."}}},
        }
    },
}

list_users: Dict[str, Any] = {
    "name": "List of users",
    "description": "Get list of users.",
    "responses": {204: {"description": "List of users empty."}, **base_responses},
}

get_user: Dict[str, Any] = {
    "name": "Get User",
    "description": "Get user by ID.",
    "responses": {
        **base_responses,
        404: {"description": "User not found."},
    },
}

update_user: Dict[str, Any] = {
    "name": "Update User",
    "description": "Update user by ID.",
    "responses": {
        **base_responses,
        404: {"description": "User not found."},
        422: response_422,
    },
}

create_user: Dict[str, Any] = {
    "name": "Create User",
    "description": "Create user.",
    "responses": {
        **base_responses,
    },
}

delete_user: Dict[str, Any] = {
    "name": "Delete User",
    "description": "Delete user.",
    "responses": {**base_responses, 404: {"description": "User not found."}},
}

__all__ = (
    "list_users",
    "get_user",
    "update_user",
    "create_user",
    "delete_user",
)
