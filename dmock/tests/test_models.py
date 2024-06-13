from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock, Rule, MockLog, Settings


class TestMock(test.TestCase):
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.the_mock = await Mock.create(name="with_rules", status="active")
        await Rule.create(mock=self.the_mock, type="2-url", operation="equals", key="/test")
        await Rule.create(mock=self.the_mock, type="4-header", operation="equals", key="hello", value="world")

    async def test_mock_created(self):
        mock = await Mock.create(name="test", status="draft")
        retrieved_mock = await Mock.get(id=mock.id)
        self.assertEqual(retrieved_mock.name, 'test')

    async def test_mock_created_with_binary_body(self):
        mock = await Mock.create(name="test2", status="active", response_body=b"hello world")
        self.assertEqual(mock.response_body, b"hello world")

    async def test_mock_created_setup(self):
        mock = await Mock.create(id=111, name="Master mock (default)",
                                 method="ANY", url="/",
                                 response_body=b"hello world",
                                 response_headers={"Content-Type": "text/plain"},
                                 status_code=200, is_default=True,
                                 labels=["default"], status="active")
        self.assertEqual(mock.name, 'Master mock (default)')
        self.assertEqual(mock.id, 111)

    # async def test_mock_get_or_create_setup(self):
    #     mock = await Mock.get_or_create(id=1111, name="Master mock (default)",
    #                                     method="ANY", url="/",
    #                                     response_body=b"hello world",
    #                                     response_headers={"Content-Type": "text/plain"},
    #                                     status_code=200, is_default=True,
    #                                     labels=["default"], status="active")
    #     self.assertEqual(mock[0].name, 'Master mock (default)')
    #     self.assertEqual(mock[0].id, 1111)

    async def test_rule_created(self):
        mock = await Mock.create(name="test2")
        rule = await Rule.create(mock=mock, type="1-default", operation="equals", key="GET")
        self.assertEqual(rule.type, '1-default')

    async def test_mock_log_created(self):
        mock = await Mock.create(name="test3")
        mock_log = await MockLog.create(mock=mock, request_method="GET", request_url="/")
        self.assertEqual(mock_log.request_method, 'GET')

    async def test_rules_accessible(self):
        rules = await self.the_mock.rules
        self.assertEqual(len(rules), 2)
