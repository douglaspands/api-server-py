from app.api import create_app
from app.core.utils.adba import AsyncDatabaseAdapter

adb = AsyncDatabaseAdapter(app=create_app())

__all__ = ('adb',)
