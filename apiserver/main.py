import os

from fastapi import FastAPI


def create_app(config_env: str = os.getenv('PYTHON_ENV', 'development')) -> FastAPI:

    from apiserver.core.config import create_config

    settings = create_config(config_env)

    from apiserver.core import openapi, routers, handlers
    from apiserver.core.databases.sqlalchemy import database

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

    handlers.init_app(app)
    routers.init_app(app)
    openapi.init_app(app)

    return app


__all__ = ('create_app',)
