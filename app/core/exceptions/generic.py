"""Core Generic Error."""
from typing import Optional


class BaseError(Exception):
    """Base Error."""

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        self.code = code or 'error'
        self.message = message
        super().__init__(self.message)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, message={self.message!r})"


class NotFoundError(BaseError):
    """Not Found Error."""

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message=message, code=code)


class BusinessLogicError(BaseError):
    """Business Logic Error."""

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message=message, code=code)


__all__ = ('BaseError',
           'NotFoundError',
           'BusinessLogicError')
