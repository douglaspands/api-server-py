import os

import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from apiserver.core import config, openapi


def test_init_app() -> None:
    app = FastAPI()
    openapi.init_app(app)
    assert callable(app.openapi)


def test_custom_openapi_1() -> None:
    app = FastAPI()
    os.environ['PYTHON_ENV'] = 'development'
    settings = config.Settings.from_env()
    res = openapi.custom_openapi(app)
    assert res == {
        'info': {
            'description': settings.SERVER_DESCRIPTION,
            'title': settings.SERVER_TITLE,
            'version': settings.SERVER_VERSION},
        'openapi': '3.0.2',
        'paths': {}}


def test_custom_openapi_2_yet_load() -> None:
    app = FastAPI()
    os.environ['PYTHON_ENV'] = 'development'
    settings = config.Settings.from_env()
    openapi.custom_openapi(app)
    res = openapi.custom_openapi(app)
    assert res == {
        'info': {
            'description': settings.SERVER_DESCRIPTION,
            'title': settings.SERVER_TITLE,
            'version': settings.SERVER_VERSION},
        'openapi': '3.0.2',
        'paths': {}}


def test_custom_openapi_3_422_to_400() -> None:
    app = FastAPI()

    @app.get('/test/{id}')
    def controller(id: int):
        return {'data': {'id': id}}

    os.environ['PYTHON_ENV'] = 'development'
    res = openapi.custom_openapi(app)

    settings = config.Settings.from_env()
    assert res == {'openapi': '3.0.2',
                   'info': {'description': settings.SERVER_DESCRIPTION,
                            'title': settings.SERVER_TITLE,
                            'version': settings.SERVER_VERSION},
                   'paths': {
                       '/test/{id}': {
                           'get': {'summary': 'Controller',
                                   'operationId': 'controller_test__id__get',
                                   'parameters': [{'required': True,
                                                   'schema': {'title': 'Id',
                                                              'type': 'integer'},
                                                   'name': 'id',
                                                   'in': 'path'}],
                                   'responses': {'200': {'description': 'Successful Response',
                                                         'content': {'application/json': {'schema': {}}}},
                                                 '400': {'description': 'Bad Request',
                                                         'content': {'application/json': {'schema': {
                                                             '$ref': '#/components/schemas/HTTPBadRequest'}}}}}}}},
                   'components': {'schemas': {'ValidationError': {'title': 'ValidationError',
                                                                  'required': ['loc', 'msg', 'type'],
                                                                  'type': 'object',
                                                                  'properties': {'loc': {'title': 'Location',
                                                                                         'type': 'array',
                                                                                         'items': {'type': 'string'}},
                                                                                 'msg': {'title': 'Message',
                                                                                         'type': 'string'},
                                                                                 'type': {'title': 'Error Type',
                                                                                          'type': 'string'}}},
                                              'HTTPBadRequest': {'title': 'HTTPBadRequest',
                                                                 'type': 'object',
                                                                 'properties': {'error': {'title': 'Error Detail',
                                                                                          'type': 'array',
                                                                                          'items': {
                                                                                              '$ref': '#/components/schemas/ValidationError'}}}}}}}
