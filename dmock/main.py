from typing import Any
from tortoise import Tortoise
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from dmock import settings
from dmock.models.setup import set_data
from aerich import Command
from pydantic import BaseModel
from dmock.api import operator, overseer
from dmock.middleware.dispatcher import dispatch_request
from dmock.settings import STATIC_ROOT

app = FastAPI()
app.mount('/assets', StaticFiles(directory=STATIC_ROOT), name='assets')
app.include_router(operator.router)
app.include_router(overseer.router)

register_tortoise(app=app,
                  config=settings.DB_CONFIG,
                  generate_schemas=True,
                  add_exception_handlers=True)


@app.on_event("startup")
async def startup_event():
    await set_data()


@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


@app.get("/")
async def root():
    return FileResponse('ui/html/index.html', media_type='text/html')


class Item(BaseModel):
    name: str
    description: str | None = None


@app.post("/items/")
async def create_item(item: Item):
    return {'ok': True, 'item': item}
