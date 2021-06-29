from core.server.bootstrap import app
from fastapi.openapi.utils import get_openapi
from pydash import _


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='API Manager',
        version='1.0.0',
        description='OpenAPI schema',
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
    _.set(openapi_schema, 'components.schemas.HTTPBadRequest',
          _.get(openapi_schema, 'components.schemas.HTTPValidationError'))
    _.set(openapi_schema, 'components.schemas.HTTPBadRequest.title', 'HTTPBadRequest')
    _.set(openapi_schema, 'components.schemas.HTTPBadRequest.properties.error',
          _.get(openapi_schema, 'components.schemas.HTTPValidationError.properties.detail'))
    _.set(openapi_schema, 'components.schemas.HTTPBadRequest.properties.error.title', 'Error Detail')
    _.get(openapi_schema, 'components.schemas.HTTPBadRequest.properties').pop('detail')
    _.get(openapi_schema, 'components.schemas').pop('HTTPValidationError')
    for schema in _.get(openapi_schema, 'components.schemas', []):
        if _.get(openapi_schema, f'components.schemas.{schema}.properties.detail'):
            _.set(openapi_schema, f'components.schemas.{schema}.properties.error',
                  _.get(openapi_schema, f'components.schemas.{schema}.properties.detail'))
            _.get(openapi_schema, f'components.schemas.{schema}.properties').pop('detail')
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
