import ormar
from core.models.ormar import BaseMeta, BaseModel


class User(BaseModel):
    class Meta(BaseMeta):
        tablename: str = 'users'

    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    username: str = ormar.String(max_length=255, unique=True)
    is_active: bool = ormar.Boolean()


__all__ = ('User',)
