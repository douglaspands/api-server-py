import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_validation_exception_handler_400_bad_request_1():
    from apiserver.core.handlers import init_app
    
    app = FastAPI()
    init_app(app)
    
    @app.get('/users/{id}')
    async def controller(id: int):
        return {'data': {'name': 'Peter', 'lastname': 'Pan'}}

    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/users/a')

    assert response.status_code == 400
    assert response.json() == {'error':[{'loc':['path','id'],'msg':'value is not a valid integer','type':'type_error.integer'}]}


@pytest.mark.asyncio
async def test_validation_exception_handler_400_bad_request_2():
    from pydantic import BaseModel
    from apiserver.core.handlers import init_app
    
    app = FastAPI()
    init_app(app)
    
    class UserInput(BaseModel):
        name: str
        lastname: str

    
    @app.post('/users')
    async def controller(user: UserInput):
        return {'data': {'name': user.name, 'lastname': user.lastname}}

    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.post('/users', json={'name': 'Peter'})

    assert response.status_code == 400
    assert response.json() == {'error':[{'loc':['body','lastname'],'msg':'field required','type':'value_error.missing'}], 'body': {'name': 'Peter'}}


@pytest.mark.asyncio
async def test_exception_handler_404_not_found():
    from apiserver.core.handlers import init_app
    from apiserver.core.exceptions.http import HTTPException as CoreHTTPException 

    app = FastAPI()
    init_app(app)
    
    @app.get('/users/{id}')
    async def controller(id: int):
        raise CoreHTTPException(status_code=404)

    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/users/1')

    assert response.status_code == 404
    assert response.json() == None


@pytest.mark.asyncio
async def test_exception_handler_422_business_error():
    from apiserver.core.handlers import init_app
    from apiserver.core.exceptions.http import HTTPException as CoreHTTPException 

    app = FastAPI()
    init_app(app)
    
    @app.get('/users/{id}')
    async def controller(id: int):
        raise CoreHTTPException(status_code=422, message='Business Error')

    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/users/1')

    assert response.status_code == 422
    assert response.json() == {'error': 'Business Error'}


@pytest.mark.asyncio
async def test_exception_handler_500_internal_error():
    from apiserver.core.handlers import init_app
    from starlette.exceptions import HTTPException as StarletteHTTPException

    app = FastAPI()
    init_app(app)
    
    @app.get('/users/{id}')
    async def controller(id: int):
        raise StarletteHTTPException(status_code=500, detail='Generic Error')

    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/users/1')

    assert response.status_code == 500
    assert response.json() == {'error': 'Generic Error'}
