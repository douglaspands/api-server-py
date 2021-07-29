"""Core Http Error."""


from starlette import status


class HttpError(Exception):
    """Http Error."""

    def __init__(self, status_code: int, message: str = None) -> None:
        self.status_code = status_code
        self.error = message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, error={self.error!r})"


class HttpNoContentError(HttpError):
    """No Content Error."""

    status_code: int = status.HTTP_204_NO_CONTENT

    def __init__(self) -> None:
        super().__init__(self.status_code, '')


class HttpUnauthorizedError(HttpError):
    """Unauthorized Error."""

    status_code: int = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str) -> None:
        super().__init__(self.status_code, message)


class HttpForbiddenError(HttpError):
    """Forbidden Error."""

    status_code: int = status.HTTP_403_FORBIDDEN

    def __init__(self, message: str) -> None:
        super().__init__(self.status_code, message)


class HttpNotFoundError(HttpError):
    """Not Found Error."""

    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(self) -> None:
        super().__init__(self.status_code, '')


class HttpUnprocessableEntityError(HttpError):
    """Unprocessable Entity Error."""

    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, message: str) -> None:
        super().__init__(self.status_code, message)


__all__ = ('HttpError',
           'HttpNoContentError',
           'HttpUnauthorizedError',
           'HttpForbiddenError',
           'HttpNotFoundError',
           'HttpUnprocessableEntityError')
