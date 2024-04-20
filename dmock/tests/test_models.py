from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock, Rules, MockLog, Settings


class TestMock(test.TestCase):
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    async def test_mock_created(self):
        mock = await Mock.create(name="test", status="draft")
        retrieved_mock = await Mock.get(id=mock.id)
        self.assertEqual(retrieved_mock.name, 'test')

    async def test_rule_created(self):
        mock = await Mock.create(name="test2")
        rule = await Rules.create(mock=mock, type="1-method", operation="equals", key="GET")
        self.assertEqual(rule.type, '1-method')

    async def test_mock_log_created(self):
        mock = await Mock.create(name="test3")
        mock_log = await MockLog.create(mock=mock, request_method="GET", request_url="/")
        self.assertEqual(mock_log.request_method, 'GET')
