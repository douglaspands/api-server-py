from unittest.mock import patch, MagicMock

from fastapi import FastAPI, APIRouter

from app.core import routers


def test_init_app_module_not_found(settings):
    app = FastAPI()
    with patch('app.core.routers.settings', settings):
        routers.init_app(app)
        assert hasattr(app, 'routes')


def test_init_app_exception(settings):
    app = FastAPI()
    with patch('app.core.routers.import_module', MagicMock(side_effect=Exception('Error'))):
        with patch('app.core.routers.logger.error') as mock_logger:
            with patch('app.core.routers.settings', settings):
                r = routers.init_app(app)
                assert len(r) == 0
                assert mock_logger.called
                assert mock_logger.call_count == len(settings.ROUTERS)


def test_init_app_ok_1(settings):
    def mock_import(*args, **kwargs):
        mock_module = MagicMock()
        mock_module.router = APIRouter()
        mock_module.router_api = APIRouter()
        return mock_module

    app = FastAPI()
    with patch('app.core.routers.import_module', mock_import):
        with patch('app.core.routers.settings', settings):
            r = routers.init_app(app)
            assert len(r) == len(settings.ROUTERS)


def test_init_app_ok_2(settings):
    def mock_import(*args, **kwargs):
        if args[0] == 'app.players':
            mock_module = MagicMock()
            mock_module.router_api = APIRouter()
            return mock_module
        elif args[0] == 'app.teams':
            mock_module = MagicMock()
            mock_module.router = APIRouter()
            return mock_module
        else:
            return None

    app = FastAPI()
    with patch('app.core.routers.import_module', mock_import):
        with patch('app.core.routers.settings', settings):
            r = routers.init_app(app)
            assert len(r) == (len(settings.ROUTERS) - 1)
