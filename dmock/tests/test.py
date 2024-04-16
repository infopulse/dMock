from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock


class TestMock(test.TestCase):
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    async def test_mock_created(self):
        mock = await Mock.create(name="Test Mock", status="active", labels="test, mock", timeout=5, method="GET",
                                 url="/test", request_headers={}, request_body="", response_headers={},
                                 response_body="", status_code=200, is_action=False, action="")
        retrieved_mock = await Mock.get(id=mock.id)
        self.assertEqual(retrieved_mock.id, 1)
