from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse
from typing import Any
from dmock.api import mock_caller as mc
from dmock.middleware.dispatcher import dispatch_request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.api_route("/mock/{path:path}",
                  methods=["GET", "HEAD, ""POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
async def mock_dispatcher(request: Request, path: str):
    raw_body = await request.body()
    body = raw_body.decode('utf-8') if raw_body else None

    return await dispatch_request(method=request.method,
                                  url=str(path),
                                  headers=dict(request.headers),
                                  body=body)

@router.api_route("/{path:path}",
                  methods=["GET", "HEAD, ""POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
async def mock_caller(request: Request, path: str):
    
    code, content = await mc.call_mock(method=request.method, url="/"+str(path))
    return JSONResponse(status_code=code, content=content)