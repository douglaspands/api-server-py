from datetime import datetime

import ormar

from apiserver.core.databases.sqlalchemy import database, metadata


class BaseModelMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class BaseModel(ormar.Model):
    class Meta(BaseModelMeta):
        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow)

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)


__all__ = ('BaseModelMeta', 'BaseModel',)
