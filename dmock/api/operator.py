from dmock.middleware.mock_manager import (get_mocks, get_mock,
                                           create_mock_manually, delete_mock_by_id as dm,
                                           edit_mock, get_rule, edit_rule, delete_rule, create_rule)
from dmock.api.schemas import MockIn, RuleIn
from fastapi import Request, APIRouter, Response
from fastapi.responses import JSONResponse
import json

router = APIRouter()


@router.get("/api/mocks")
async def list_mocks():
    mocks = await get_mocks()
    return {
        "mocks": [await mock.to_dict() for mock in mocks],
        "total": len(mocks)
    }


@router.get("/api/mocks/{mock_id}/rules")
async def list_rules(mock_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})
    rules = await mock.rules
    return {"rules": [await rule.to_dict() for rule in rules],
            "total": len(rules)}


@router.get("/api/mocks/{mock_id}/logs")
async def list_logs(mock_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})
    logs = await mock.logs
    return {"logs": [await log.to_dict() for log in logs],
            "total": len(logs)}


@router.get("/api/mocks/{mock_id}/rules/{rule_id}")
async def get_rule_api(mock_id: int, rule_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})

    rule = await get_rule(rule_id)
    if rule is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})
    return await rule.to_dict()


@router.post("/api/mocks")
async def create_mock_api(mock_request: MockIn, request: Request):
    try:
        mock = await create_mock_manually(**mock_request.dict())
        return await mock.to_dict()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.delete("/api/mocks/{mock_id}")
async def delete_mock_api(mock_id: int):
    try:
        await dm(mock_id)
        return Response(status_code=204)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/api/mocks/{mock_id}")
async def get_mock_api(mock_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})
    return await mock.to_dict()


@router.put("/api/mocks/{mock_id}")
async def update_mock_api(mock_request: MockIn, mock_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})
    mock = await edit_mock(mock, **mock_request.dict())
    return await mock.to_dict()


@router.post("/api/mocks/{mock_id}/rules")
async def create_rule_api(mock_id: int, rule_request: RuleIn):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})

    try:
        rule = await create_rule(mock, **rule_request.dict())
        return await rule.to_dict()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.put("/api/mocks/{mock_id}/rules/{rule_id}")
async def update_rule_api(mock_id: int, rule_id: int, rule_request: RuleIn):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})

    rule = await get_rule(rule_id)
    if rule is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})

    rule = await edit_rule(rule, **rule_request.dict())
    return await rule.to_dict()


@router.delete("/api/mocks/{mock_id}/rules/{rule_id}")
async def delete_rule_api(mock_id: int, rule_id: int):
    mock = await get_mock(mock_id)
    if mock is None:
        return JSONResponse(status_code=404, content={"error": "Mock not found"})

    rule = await get_rule(rule_id)
    if rule is None:
        return JSONResponse(status_code=404, content={"error": "Rule not found"})

    try:
        await delete_rule(rule)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    return Response(status_code=204)
