from fastapi import FastAPI
from core.config import settings
from core.databases.sqlalchemy import database

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
