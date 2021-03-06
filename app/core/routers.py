"""Core Routers Scan."""
import logging
from typing import List
from importlib import import_module

from fastapi import FastAPI, APIRouter

from app.config import settings

logger = logging.getLogger(__name__)


def init_app(app: FastAPI) -> List[APIRouter]:
    """Configure routers in FastApi App.

    Args:
        app (FastAPI): FastAPI instance.

    Returns:
        List[APIRouter]: List of routers.
    """
    routers: List[APIRouter] = []
    for router_path in settings.ROUTERS:
        try:
            mr = router_path.split(":")
            module_name = mr[0]
            router_name = mr[1] if len(mr) > 1 else "router"
            router = getattr(import_module(f"app.{module_name}"), router_name, None)

            if isinstance(router, APIRouter):
                app.include_router(router, prefix=settings.API_PREFIX)
                routers.append(router)

        except ModuleNotFoundError:
            logger.warning(f"Router '{router_path}' not found!")

        except Exception as err:
            logger.error(err, exc_info=True)

    return routers


__all__ = ("init_app",)
