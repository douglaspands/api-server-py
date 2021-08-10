"""Users OpenApiDocs."""
from typing import Any, Dict

get_token: Dict[str, Any] = {
    "name": "Get token.",
    "description": "Get token for system access.",
    "responses": {400: {"description": "Bad request."}, 401: {"description": "Unauthorized access."}},
}


__all__ = ("get_token",)
