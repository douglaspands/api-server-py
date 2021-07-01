import ormar
from core.models.ormar import BaseMeta
from datetime import datetime
from sqlalchemy import func


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'user'

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    username: str = ormar.String(max_length=255, unique=True)
    active: bool = ormar.Boolean()
    created_at: datetime = ormar.DateTime(server_default=func.now())
    updated_at: datetime = ormar.DateTime(server_default=func.now())


__all__ = ('User',)
