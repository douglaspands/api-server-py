from app.api import create_app
from app.core.utils.adba import AsyncDatabaseByApp

adb = AsyncDatabaseByApp(app=create_app())

__all__ = ('adb',)
