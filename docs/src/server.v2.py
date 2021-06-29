from fastapi import FastAPI, Request, status
from core.config import settings
from core.router import finder
from core.database.sqlalchemy import database
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from pydash import _

app = FastAPI(
    openapi_url=f'{settings.API_PREFIX}/openapi.json',
    # docs_url=None,
    # redoc_url=f'{settings.API_PREFIX}/documentation',
    docs_url=f'{settings.API_PREFIX}/docs',
    redoc_url=f'{settings.API_PREFIX}/redoc',
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'error': exc.errors(), 'body': exc.body}),
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='DPANDS API Manager',
        version='1.0.0',
        description='OpenAPI schema from DPANDS',
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
          _.get(openapi_schema, 'components.schemas.HTTPBadRequest.properties.detail'))
    _.set(openapi_schema, 'components.schemas.HTTPBadRequest.properties.error.title', 'Error Detail')
    _.get(openapi_schema, 'components.schemas.HTTPBadRequest.properties').pop('detail')
    _.get(openapi_schema, 'components.schemas').pop('HTTPValidationError')
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

for r in finder():
    app.include_router(r, prefix=settings.API_PREFIX)


__all__ = ('app',)
