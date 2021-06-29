import logging
from importlib import import_module

from fastapi import APIRouter
from core.config import settings
from core.server.bootstrap import app

logger = logging.getLogger(__name__)


for router_path in settings.ROUTERS:
    try:
        mr = router_path.split(':')
        module_name = mr[0]
        router_name = mr[1] if len(mr) > 1 else 'router'
        router = getattr(import_module(module_name), router_name, None)
        if isinstance(router, APIRouter):
            app.include_router(router, prefix=settings.API_PREFIX)

    except ModuleNotFoundError:
        pass

    except Exception as err:
        logger.error(err, exc_info=True)
