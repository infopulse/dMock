from typing import Any
from tortoise import Tortoise
from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise
from dmock import settings
from dmock.models.setup import set_data
from aerich import Command
from fastapi.responses import FileResponse
from middleware.dispatcher import dispatch_request

app = FastAPI()
register_tortoise(app=app,
                  config=settings.DB_CONFIG,
                  generate_schemas=True,
                  add_exception_handlers=True)


@app.middleware("http")
async def intercept_requests(request: Request, call_next: Any):
    raw_body = await request.body()
    body = raw_body.decode('utf-8') if raw_body else None

    if request.url.path.startswith('/mock'):
        return await dispatch_request(method=request.method,
                                      url=str(request.url),
                                      headers=dict(request.headers),
                                      body=body)
    elif request.url.path.startswith('/api'):
        return await call_next(request)
    else:
        FileResponse('ui/html/404.html', media_type='text/html')


@app.on_event("startup")
async def startup_event():
    await set_data()


@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


@app.get("/api/123")
async def root():
    return {'api': '123'}


@app.get("/")
async def root():
    return FileResponse('ui/html/index.html', media_type='text/html')
