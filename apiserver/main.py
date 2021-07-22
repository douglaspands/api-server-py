from fastapi import FastAPI

from apiserver.core import openapi, routers, handlers
from apiserver.core.config import settings
from apiserver.core.databases.sqlalchemy import database


def create_app() -> FastAPI:

    app = FastAPI(
        openapi_url=f'{settings.API_PREFIX}/openapi.json',
        # docs_url=None,
        # redoc_url=f'{settings.API_PREFIX}/documentation',
        docs_url=f'{settings.API_PREFIX}/docs',
        redoc_url=f'{settings.API_PREFIX}/redoc',
    )

    @app.on_event('startup')
    async def startup() -> None:
        await database.connect()

    @app.on_event('shutdown')
    async def shutdown() -> None:
        await database.disconnect()

    handlers.init_app(app)
    routers.init_app(app)
    openapi.init_app(app)

    return app


__all__ = ('create_app',)
