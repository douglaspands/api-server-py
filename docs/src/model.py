from datetime import datetime

import ormar
from sqlalchemy import func
from core.model.ormar import BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'user'

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=255)
    password: str = ormar.String(max_length=255)
    username: str = ormar.String(max_length=255)
    created_at: datetime = ormar.DateTime(server_default=func.now())
    updated_at: datetime = ormar.DateTime(server_default=func.now())


__all__ = ('User',)
