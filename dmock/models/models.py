from tortoise.models import Model
from tortoise import fields


class Mock(Model):
    # service
    id = fields.IntField(pk=True, generated=True)
    name = fields.TextField()
    status = fields.TextField(default='draft')  ## draft, active, inactive
    labels = fields.JSONField(null=True)
    delay = fields.IntField(default=0)
    is_default = fields.BooleanField(default=False)
    priority = fields.IntField(null=True)

    # HTTP
    method = fields.TextField(null=True)
    url = fields.TextField(null=True)

    response_headers = fields.JSONField(null=True)
    response_body = fields.TextField(null=True)
    status_code = fields.IntField(null=True)

    is_action = fields.BooleanField(default=False)
    action = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    requests_count = fields.IntField(default=0)

    async def to_dict(self) -> dict:
        rules = await self.rules
        logs = await self.logs
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "labels": self.labels,
            "delay": self.delay,
            # "isDefault": self.is_default,
            "priority": self.priority,
            "method": self.method,
            "url": self.url,
            "responseHeaders": self.response_headers,
            "responseBody": self.response_body,
            "statusCode": self.status_code,
            "isAction": self.is_action,
            "action": self.action,
            "createdAt": self.created_at,
            "requestsCount": self.requests_count,
            "rulesNumber": len(rules),
            "logsNumber": len(logs)
        }

    class Meta:
        table = "mock"
        ordering = ["id"]


# for static mock data
class Rules(Model):
    id = fields.IntField(pk=True, generated=True)
    mock = fields.ForeignKeyField("models.Mock", related_name="rules", on_delete=fields.CASCADE)
    is_active = fields.BooleanField(default=True)
    type = fields.TextField()  # 1-default, 2-url, 3-json, 3-body, 4-headers. makes priority
    operation = fields.TextField()  # contains, in, equals, regex, starts_with, ends_with
    key = fields.TextField()

    async def to_dict(self) -> dict:
        mock = await self.mock
        return {
            "id": self.id,
            "mockId": mock.id,
            "is_active": self.is_active,
            "type": self.type,
            "operation": self.operation,
            "key": self.key,
        }

    class Meta:
        table = "rules"
        ordering = ["type", "-is_active", "id"]


class MockLog(Model):
    id = fields.IntField(pk=True, generated=True)
    mock = fields.ForeignKeyField("models.Mock", related_name="logs", on_delete=fields.CASCADE)

    request_method = fields.TextField()
    request_url = fields.TextField()
    request_headers = fields.JSONField(default={})
    request_body = fields.TextField(null=True)

    response_headers = fields.JSONField(null=True)
    response_body = fields.TextField(null=True)
    status_code = fields.IntField(default=200)
    timestamp = fields.DatetimeField(auto_now_add=True)
    mocks_matched_ids = fields.JSONField(default=[])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "mockId": self.mock.id,
            "requestMethod": self.request_method,
            "requestUrl": self.request_url,
            "requestHeaders": self.request_headers,
            "requestBody": self.request_body,
            "responseHeaders": self.response_headers,
            "responseBody": self.response_body,
            "statusCode": self.status_code,
            "timestamp": self.timestamp,
            "mocksMatchedIds": self.mocks_matched_ids,
        }

    class Meta:
        table = "mock_log"
        ordering = ["-timestamp"]


class Settings(Model):
    id = fields.IntField(pk=True)
    key = fields.TextField()
    value = fields.TextField()

    class Meta:
        table = "settings"
        ordering = ["id"]
