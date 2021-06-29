import os
import logging
from typing import List
from importlib import import_module

from fastapi import APIRouter

logger = logging.getLogger(__name__)


def finder() -> List[APIRouter]:

    unallowed_dirs = ('__pycache__')

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    apps_dir = [f for f in os.listdir(root_dir)
                if not os.path.isfile(os.path.join(root_dir, f)) and f not in unallowed_dirs]

    routers: List[APIRouter] = []

    for app in apps_dir:
        try:
            module = import_module(f'{app}.controller')
            router = getattr(module, 'router', None)
            if isinstance(router, APIRouter):
                routers.append(router)

        except ModuleNotFoundError:
            pass

        except Exception as err:
            logger.error(err, exc_info=True)

    return routers


__all__ = ('finder',)
