from typing import Any, Dict
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from core.server.bootstrap import app


def create_context(exc: object) -> Dict[str, Any]:
    content = {}
    if hasattr(exc, 'errors'):
        content['error'] = exc.errors()
    else:
        content['error'] = exc.detail
    if getattr(exc, 'body', None):
        content['body'] = exc.body
    return content


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = create_context(exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(content),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    content = create_context(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(content),
    )
