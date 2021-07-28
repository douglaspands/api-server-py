"""Core OpenApi Docs."""
from typing import Any, Dict

from pydash import _
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config import settings


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

    for path in openapi_schema['paths']:
        for method in _.get(openapi_schema, f'paths.{path}', []):
            if _.get(openapi_schema, f'paths.{path}.{method}.responses.422.description') == 'Validation Error':
                _.set(openapi_schema, f'paths.{path}.{method}.responses.400',
                      _.get(openapi_schema, f'paths.{path}.{method}.responses.422'))
                _.set(openapi_schema, f'paths.{path}.{method}.responses.400.description', 'Bad Request')
                _.set(openapi_schema, f'paths.{path}.{method}.responses.400.content.application/json.schema.$ref',
                      '#/components/schemas/HTTPBadRequest')
                _.get(openapi_schema, f'paths.{path}.{method}.responses').pop('422')

    for schema in _.get(openapi_schema, 'components.schemas', []):
        if _.get(openapi_schema, f'components.schemas.{schema}.properties.detail'):
            _.set(openapi_schema, f'components.schemas.{schema}.properties.error',
                  _.get(openapi_schema, f'components.schemas.{schema}.properties.detail'))
            _.get(openapi_schema, f'components.schemas.{schema}.properties').pop('detail')

    if _.get(openapi_schema, 'components.schemas.HTTPValidationError'):
        _.set(openapi_schema,
              'components.schemas.HTTPBadRequest',
              _.get(openapi_schema, 'components.schemas.HTTPValidationError'))
        _.set(openapi_schema,
              'components.schemas.HTTPBadRequest.title',
              'HTTPBadRequest')
        _.set(openapi_schema,
              'components.schemas.HTTPBadRequest.properties.error.title',
              'Error Detail')
        _.get(openapi_schema, 'components.schemas').pop('HTTPValidationError')

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def init_app(app: FastAPI) -> None:
    """Configure openapi docs in FastApi App.

    Args:
        app (FastAPI): FastAPI instance.
    """
    setattr(app, 'openapi', lambda: custom_openapi(app))


__all__ = ('init_app',)
