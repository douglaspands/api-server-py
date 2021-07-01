import ormar
from core.databases.sqlalchemy import database, metadata


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


__all__ = ('BaseMeta')
