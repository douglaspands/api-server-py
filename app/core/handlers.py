from typing import Any, Dict, Union

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions.http import HTTPException as CoreHTTPException


def init_app(app: FastAPI) -> None:

    def create_context(exc: Union[RequestValidationError, StarletteHTTPException]) -> Dict[str, Any]:
        content: Dict[str, Any] = {}
        if isinstance(exc, RequestValidationError):
            content['error'] = exc.errors()
            if getattr(exc, 'body', None):
                content['body'] = exc.body
        else:
            content['error'] = exc.detail
        return content

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        content = create_context(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(content),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        content = create_context(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(content),
        )

    @app.exception_handler(CoreHTTPException)
    async def http_core_exception_handler(request: Request, exc: CoreHTTPException) -> JSONResponse:
        data: Dict[str, Any] = {'status_code': exc.status_code}
        if getattr(exc, 'error', None):
            data['content'] = jsonable_encoder({'error': exc.error})
        return JSONResponse(**data)


__all__ = ('init_app',)
