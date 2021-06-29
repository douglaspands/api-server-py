import http


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str = None) -> None:
        if message is None:
            message = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.error = message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, error={self.error!r})"


__all__ = ('HTTPException',)
