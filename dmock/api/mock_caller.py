from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict
import json
import dmock.middleware.mock_manager as man
from dmock.models.models import Mock, Rules
import sys
import traceback
from string import Template

app = FastAPI()

async def call_mock(method, url):
    #TO DO GLOBAL ARGUMENTS
    mocks = await man.get_mocks()
    for mock in mocks:
        if mock.method == method:
            if mock.url == url:
                target = mock
    
    responce = await execute_code(target.action)
    return target.status_code, {"responce":responce}

async def execute_code(body: str, **kwargs) -> str:
    template = Template(body)
    code_to_execute = template.safe_substitute(**kwargs)
    
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        exec(code_to_execute, {}, {})
        result = mystdout.getvalue()
    except Exception as e:
        result = f"Error: {str(e)}\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout
    
    return result