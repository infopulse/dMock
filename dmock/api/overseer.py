from fastapi import FastAPI, Request, APIRouter, Response
from fastapi.responses import FileResponse
from typing import Any
from dmock.middleware.dispatcher import dispatch_request

router = APIRouter()


@router.api_route("/mock/{path:path}",
                  methods=["GET", "HEAD, ""POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
async def mock_dispatcher(request: Request, path: str):
    raw_body = await request.body()
    # TODO add query params
    body = raw_body.decode('utf-8') if raw_body else None
    result = await dispatch_request(method=request.method,
                                    url=str(path),
                                    headers=dict(request.headers),
                                    body=body,
                                    query_params=dict(request.query_params))
    response = Response(status_code=result["status_code"],
                        headers=result["headers"],
                        content=result["body"])
    return response
