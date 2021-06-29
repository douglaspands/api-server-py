import ormar
from core.database.sqlalchemy import database, metadata


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


__all__ = ('BaseMeta')
