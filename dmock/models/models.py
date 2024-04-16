from tortoise.models import Model
from tortoise import fields


class Mock(Model):
    # service
    id = fields.IntField(pk=True)
    name = fields.TextField()
    status = fields.TextField()  ## draft, active, inactive
    labels = fields.TextField()  ## comma separated
    timeout = fields.IntField()
    aaa = fields.TextField()

    # HTTP
    method = fields.TextField()
    url = fields.TextField()
    request_headers = fields.JSONField()
    request_body = fields.TextField()
    response_headers = fields.JSONField()
    response_body = fields.TextField()
    status_code = fields.IntField()

    is_action = fields.BooleanField()
    action = fields.TextField()

    class Meta:
        table = "mock"


class MockLog(Model):
    id = fields.IntField(pk=True)
    mock = fields.ForeignKeyField("models.Mock", related_name="logs")
    request_headers = fields.JSONField()
    request_body = fields.TextField()
    response_headers = fields.JSONField()
    response_body = fields.TextField()
    status_code = fields.IntField()

    class Meta:
        table = "mock_log"


# for static mock data
class Rules(Model):
    id = fields.IntField(pk=True)
    mock = fields.ForeignKeyField("models.Mock", related_name="rules")
    is_active = fields.BooleanField()
    type = fields.TextField()  # 1-method, 2-url, 3-body, 4-headers. makes priority
    operation = fields.TextField()  # contains, equals, regex, starts_with, ends_with
    key = fields.TextField()

    class Meta:
        table = "rules"
        ordering = ["type", "-is_active", "id"]


class Settings(Model):
    id = fields.IntField(pk=True)
    key = fields.TextField()
    value = fields.TextField()

    class Meta:
        table = "settings"
        ordering = ["id"]
