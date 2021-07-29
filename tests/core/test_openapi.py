from fastapi import FastAPI

from app.core import openapi


def test_init_app() -> None:
    app = FastAPI()
    openapi.init_app(app)
    assert callable(app.openapi)


def test_custom_openapi_1(settings) -> None:
    app = FastAPI()
    res = openapi.custom_openapi(app)
    assert res == {
        "components": {
            "schemas": {
                "HTTPUnprocessableEntity": {
                    "description": "Http unprocessable entity error.",
                    "properties": {
                        "error": {
                            "description": "Error message description.",
                            "title": "Error",
                            "type": "string"
                        }
                    },
                    "required": [
                        "error"
                    ],
                    "title": "HTTPUnprocessableEntity",
                    "type": "object"
                }
            }
        },
        "info": {
            "description": "OpenAPI schema",
            "title": "API Manager",
            "version": "1.0.0"
        },
        "openapi": "3.0.2",
        "paths": {}
    }


def test_custom_openapi_2_yet_load(settings) -> None:
    app = FastAPI()
    openapi.custom_openapi(app)
    res = openapi.custom_openapi(app)
    assert res == {
        "components": {
            "schemas": {
                "HTTPUnprocessableEntity": {
                    "description": "Http unprocessable entity error.",
                    "properties": {
                        "error": {
                            "description": "Error message description.",
                            "title": "Error",
                            "type": "string"
                        }
                    },
                    "required": [
                        "error"
                    ],
                    "title": "HTTPUnprocessableEntity",
                    "type": "object"
                }
            }
        },
        "info": {
            "description": "OpenAPI schema",
            "title": "API Manager",
            "version": "1.0.0"
        },
        "openapi": "3.0.2",
        "paths": {}
    }

def test_custom_openapi_3_422_to_400(settings) -> None:
    app = FastAPI()

    @app.get('/test/{id}')
    def controller(id: int):
        return {'data': {'id': id}}

    res = openapi.custom_openapi(app)

    assert res == {
        "components": {
            "schemas": {
                "HTTPBadRequest": {
                    "properties": {
                        "error": {
                            "description": "List of the validation errors.",
                            "items": {
                                "$ref": "#/components/schemas/ValidationError"
                            },
                            "title": "Error",
                            "type": "array"
                        }
                    },
                    "title": "HTTPBadRequest",
                    "type": "object"
                },
                "HTTPUnprocessableEntity": {
                    "description": "Http unprocessable entity error.",
                    "properties": {
                        "error": {
                            "description": "Error message description.",
                            "title": "Error",
                            "type": "string"
                        }
                    },
                    "required": [
                        "error"
                    ],
                    "title": "HTTPUnprocessableEntity",
                    "type": "object"
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "type": "string"
                            },
                            "title": "Location",
                            "type": "array"
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string"
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string"
                        }
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type"
                    ],
                    "title": "ValidationError",
                    "type": "object"
                }
            }
        },
        "info": {
            "description": "OpenAPI schema",
            "title": "API Manager",
            "version": "1.0.0"
        },
        "openapi": "3.0.2",
        "paths": {
            "/test/{id}": {
                "get": {
                    "operationId": "controller_test__id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "id",
                            "required": True,
                            "schema": {
                                "title": "Id",
                                "type": "integer"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {}
                                }
                            },
                            "description": "Successful Response"
                        },
                        "400": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPBadRequest"
                                    }
                                }
                            },
                            "description": "Bad Request"
                        }
                    },
                    "summary": "Controller"
                }
            }
        }
    }
