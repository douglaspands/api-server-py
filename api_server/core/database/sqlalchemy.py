import databases
import sqlalchemy
from core.config import settings

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = sqlalchemy.MetaData()


__all__ = ('database', 'metadata',)
