"""Core Handlers."""
from typing import Any, Dict, Union

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions.http import HttpError as CoreHTTPException


def init_app(app: FastAPI) -> None:
    """Configure handlers in FastApi App.

    Args:
        app (FastAPI): FastApi instance.
    """

    def create_context(exc: Union[RequestValidationError, StarletteHTTPException]) -> Dict[str, Any]:
        """Create response context.

        Args:
            exc (Union[RequestValidationError, StarletteHTTPException]): Http Exceptions.

        Returns:
            Dict[str, Any]: Context response.
        """
        content: Dict[str, Any] = {}
        if isinstance(exc, RequestValidationError):
            content["error"] = exc.errors()
            if getattr(exc, "body", None):
                content["body"] = exc.body
        else:
            content["error"] = exc.detail
        return content

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Format response for validation exception.

        Args:
            request (Request): Request's context.
            exc (RequestValidationError): Validation exception.

        Returns:
            JSONResponse: Json data for validation error.
        """
        content = create_context(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(content),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Format generic exceptions.

        Args:
            request (Request): Request's context.
            exc (StarletteHTTPException): Scarlette exception.

        Returns:
            JSONResponse: Json data for generic error.
        """
        content = create_context(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(content),
        )

    @app.exception_handler(CoreHTTPException)
    async def http_core_exception_handler(request: Request, exc: CoreHTTPException) -> JSONResponse:
        """Format core exception.

        Args:
            request (Request): Request's context.
            exc (CoreHTTPException): Core Exception.

        Returns:
            JSONResponse: Json data for core error.
        """
        data: Dict[str, Any] = {"status_code": exc.status_code}
        if getattr(exc, "error", None):
            data["content"] = jsonable_encoder({"error": exc.error})
        return JSONResponse(**data)


__all__ = ("init_app",)
