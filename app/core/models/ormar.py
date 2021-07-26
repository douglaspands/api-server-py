from __future__ import annotations

from typing import Any, TypeVar
from datetime import datetime

import ormar

from app.core.databases.sqlalchemy import database, metadata


class BaseModelMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


T = TypeVar('T', bound='BaseModel')


class BaseModel(ormar.Model):
    class Meta(BaseModelMeta):
        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow)

    async def update(self: T, *args: Any, **kwargs: Any) -> T:
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)


__all__ = ('BaseModelMeta', 'BaseModel',)
