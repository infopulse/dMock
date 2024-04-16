from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dmock import settings
from aerich import Command


app = FastAPI()
register_tortoise(app=app,
                  config=settings.DB_CONFIG,
                  generate_schemas=True,
                  add_exception_handlers=True)


@app.on_event("startup")
async def startup_event():
    command = Command(tortoise_config=settings.DB_CONFIG, app='models')
    await command.init()
    await command.init_db(safe=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}
