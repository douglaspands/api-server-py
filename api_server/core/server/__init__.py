from importlib import import_module

from core.server.bootstrap import app

import_module('core.server.handle')
import_module('core.server.router')
import_module('core.server.doc')

__all__ = ('app',)
