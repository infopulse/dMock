from fastapi import FastAPI, Request
from typing import Dict
import dmock.middleware.dispatcher as dis

app = FastAPI()

@app.middleware("http")
async def intercept_requests(request: Request, call_next):
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    body = str(request.body)

    dis.dispatch_request(method, url, headers, body)