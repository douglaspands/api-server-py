from datetime import datetime

import ormar
from sqlalchemy import func
from core.databases.sqlalchemy import database, metadata


class BaseModelMixin:
    id: int = ormar.Integer(primary_key=True)
    created_at: datetime = ormar.DateTime(server_default=func.now())
    updated_at: datetime = ormar.DateTime(server_default=func.now())


class BaseModel(ormar.Model, BaseModelMixin):
    async def update(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super(BaseModel, self).update(*args, **kwargs)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


__all__ = ('BaseMeta', 'BaseModel',)
