from tortoise import Tortoise
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dmock import settings
from dmock.models.setup import set_data
from aerich import Command

app = FastAPI()
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
    return {"message": "Hello World"}
