from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dmock.models.setup import init

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init()


# register_tortoise(
#     app,
#     db_url='sqlite://db.sqlite3',
#     modules={'models': ['__main__']},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )

@app.get("/")
async def root():
    return {"message": "Hello World"}
