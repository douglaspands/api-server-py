"""Core OpenApi Docs."""
import re
import json
from typing import Any, Dict

from pydash import _
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config import settings

HTTP_UNPROCESSABLE_ENTITY = {
    "title": "HTTPUnprocessableEntity",
    "description": "Http unprocessable entity error.",
    "required": ["error"],
    "type": "object",
    "properties": {
        "error": {"title": "Error", "description": "Error message description.", "type": "string"},
    },
}


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """Customize openapi docs.

    Args:
        app (FastAPI): FastApi instance.

    Returns:
        Dict[str, Any]: Openapi data.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.SERVER_TITLE,
        version=settings.SERVER_VERSION,
        description=settings.SERVER_DESCRIPTION,
        routes=app.routes,
    )

    for path in openapi_schema.get("paths", {}):
        for method in _.get(openapi_schema, f"paths.{path}", []):
            if _.get(openapi_schema, f"paths.{path}.{method}.responses.422.description") == "Validation Error":
                _.set(
                    openapi_schema,
                    f"paths.{path}.{method}.responses.400",
                    _.get(openapi_schema, f"paths.{path}.{method}.responses.422"),
                )
                _.get(openapi_schema, f"paths.{path}.{method}.responses").pop("422")

    changes: Dict[str, str] = {}

    changes["Validation Error"] = "Bad Request"
    changes["HTTPValidationError"] = "HTTPBadRequest"

    regex_name_with_dot = re.compile(r"(?<=\[)(\w+(\.\w+){1,})(?=\])")

    _.set(openapi_schema, "components.schemas.HTTPUnprocessableEntity", HTTP_UNPROCESSABLE_ENTITY)

    for schema in _.get(openapi_schema, "components.schemas", {}):
        title = _.get(openapi_schema, "components.schemas").get(schema, {}).get("title", "")

        if schema == "HTTPValidationError":
            _.set(
                openapi_schema,
                f"components.schemas.{schema}.properties.error",
                _.get(openapi_schema, f"components.schemas.{schema}.properties.detail"),
            )
            _.set(openapi_schema, f"components.schemas.{schema}.properties.error.title", "Error")
            _.set(
                openapi_schema,
                f"components.schemas.{schema}.properties.error.description",
                "List of the validation errors.",
            )
            _.get(openapi_schema, f"components.schemas.{schema}.properties").pop("detail")

        elif "_" in title:
            new_title = _.camel_case(title)
            new_title = new_title[:1].capitalize() + new_title[1:]
            changes[title] = new_title

        elif "." in title:
            name = regex_name_with_dot.findall(title)[0][0]
            changes[title] = title.replace(name, name.split(".").pop())

    openapi_text = json.dumps(openapi_schema)

    for k, v in changes.items():
        openapi_text = openapi_text.replace(k, v)

    openapi_schema = json.loads(openapi_text)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def init_app(app: FastAPI) -> None:
    """Configure openapi docs in FastApi App.

    Args:
        app (FastAPI): FastAPI instance.
    """
    setattr(app, "openapi", lambda: custom_openapi(app))


__all__ = ("init_app",)
