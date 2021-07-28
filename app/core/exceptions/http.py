"""Core Exceptions."""


class HttpError(Exception):
    """Http Error."""

    def __init__(self, status_code: int, message: str = None) -> None:
        self.status_code = status_code
        self.error = message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, error={self.error!r})"


__all__ = ('HttpError',)
