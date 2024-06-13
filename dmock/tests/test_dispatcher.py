from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock, Rule, MockLog, Settings
from dmock.middleware.mock_manager import get_mock, get_mocks, create_rule, create_mock_manually
from dmock.middleware.dispatcher import dispatch_request
from dmock.models.setup import set_data


class TestMock(test.TestCase):
    mock: Mock
    default_mock: Mock
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.default_mock = await set_data()
        mock = {
            "name": "Test 1",
            "method": "GET",
            "url": "/test",
            "status": "active",
            "response_body": "test 1",
            "response_headers": {"Content-Type": "text/plain"},
            "status_code": 200,
            "rules": [
                {"type": "2-url", "operation": "equals", "key": "/test"}
            ]
        }
        self.mock = await create_mock_manually(**mock)

    async def test_no_duplicate_setup(self):
        mocks = await get_mocks()
        counter = sum(1 for _ in mocks if _.method == "ANY")
        self.assertEqual(counter, 1)

    async def test_dispatch_get(self):
        request = {
            "method": "GET",
            "url": "/test",
            "headers": {},
            "body": ""
        }
        response = await dispatch_request(**request)
        self.assertEqual(response["mock_id"], self.mock.id)

