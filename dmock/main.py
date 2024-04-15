from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

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
