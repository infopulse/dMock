from fastapi import FastAPI, Request
from typing import Dict
import dmock.middleware.dispatcher as dis
import dmock.api.operator as op

app = FastAPI()


@app.middleware("http")
async def intercept_requests(request: Request, call_next):
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    body = str(request.body)

    if request.url.path == "/mock":
        responce = await dis.dispatch_request(method, url, headers, body)
    elif request.url.path == "/api":
        responce = await op.api_dispatcher(method, url, headers, body)
    elif request.url.path == "/":
        ...
    else:
        responce = {"status_code": 400}
    return responce
