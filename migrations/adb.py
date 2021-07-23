from apiserver.main import create_app
from apiserver.core.utils.adba import AsyncDatabaseByApp

adb = AsyncDatabaseByApp(app=create_app())

__all__ = ('adb',)
