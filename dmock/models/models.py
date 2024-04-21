from tortoise.models import Model
from tortoise import fields


class Mock(Model):
    # service
    id = fields.IntField(pk=True)
    name = fields.TextField()
    status = fields.TextField(default='draft')  ## draft, active, inactive
    labels = fields.JSONField(default=[])
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

    class Meta:
        table = "mock"
        ordering = ["id"]


# for static mock data
class Rules(Model):
    id = fields.IntField(pk=True)
    mock = fields.ForeignKeyField("models.Mock", related_name="rules", on_delete=fields.CASCADE)
    is_active = fields.BooleanField(default=True)
    type = fields.TextField()  # 1-default, 2-url, 3-json, 3-body, 4-headers. makes priority
    operation = fields.TextField()  # contains, in, equals, regex, starts_with, ends_with
    key = fields.TextField()
    erroneous = fields.BooleanField(default=False)

    class Meta:
        table = "rules"
        ordering = ["type", "-is_active", "id"]


class MockLog(Model):
    id = fields.IntField(pk=True)
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
