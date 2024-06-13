from typing import Optional
from pydantic import BaseModel, field_validator as validator, ValidationError, conint, Field


class RuleIn(BaseModel):
    type: str = Field(..., alias="type")
    operation: str = Field(..., alias="operation")
    key: str = Field(..., alias="key")
    is_active: Optional[bool] = Field(True, alias="isActive")

    @validator('type')
    def validate_type(cls, value):
        if value not in ["2-url", "3-json", "3-body", "4-header"]:
            raise ValidationError("Invalid type")
        return value

    @validator('operation')
    def validate_operation(cls, value):
        if value not in ["contains", "in", "equals", "regex", "starts_with", "ends_with"]:
            raise ValidationError("Invalid operation")
        return value


class MockIn(BaseModel):
    name: str
    status: str
    method: str
    url: Optional[str] = Field(None, alias="url")
    labels: Optional[list[str]] = Field(None, alias="labels")
    delay: Optional[int] = Field(0, alias="delay", ge=0)
    priority: Optional[int] = Field(None, alias="priority", ge=0)
    response_headers: Optional[dict] = Field(None, alias="responseHeaders")
    response_body: Optional[str] = Field(None, alias="responseBody")
    status_code: Optional[int] = Field(None, alias="statusCode", ge=100, le=599)
    is_action: Optional[bool] = Field(False, alias="isAction")
    action: Optional[str] = Field(None, alias="action")
    rules: Optional[list[RuleIn]] = Field([], alias="rules")

    @validator('status')
    def validate_status(cls, value):
        if value not in ["draft", "active", "inactive"]:
            raise ValidationError("Invalid status")
        return value

    @validator('method')
    def validate_method(cls, value):
        if value not in ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]:
            raise ValueError("Invalid method")
        return value
