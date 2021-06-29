# from fastapi import FastAPI, Request, status
from fastapi import FastAPI
from core.config import settings
from core.router import finder
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from fastapi.openapi.utils import get_openapi
from core.database.sqlalchemy import database

app = FastAPI(
    title='DPANDS API Manager',
    version='1.0.0',
    description='OpenAPI schema from DPANDS',
    openapi_url=f'{settings.API_PREFIX}/openapi.json',
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
#     )


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title='DPANDS API Manager',
#         version='1.0.0',
#         description='OpenAPI schema from DPANDS',
#         routes=app.routes,
#     )
#     for path in openapi_schema['paths']:
#         for method in openapi_schema['paths'][path]:
#             if openapi_schema['paths'][path][method]['responses'].get('422', {}).get('description', '') == 'Validation Error':
#                 openapi_schema['paths'][path][method]['responses']['400'] = openapi_schema['paths'][path][method]['responses']['422']
#                 openapi_schema['paths'][path][method]['responses']['400']['description'] = 'Bad Request'
#                 openapi_schema['paths'][path][method]['responses'].pop('422')
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi


for r in finder():
    app.include_router(r, prefix=settings.API_PREFIX)


__all__ = ('app',)
