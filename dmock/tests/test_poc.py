from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock, Rule, MockLog, Settings
from dmock.middleware.mock_manager import get_mock


class TestMock(test.TestCase):
    mock: Mock

    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.mock = await Mock.create(name="test")

    async def test_get_mock(self):
        exist = await get_mock(1)
        self.assertEqual(exist, self.mock)
        not_existed = await get_mock(2)
        self.assertIsNone(not_existed)

    async def test_get_mock_cached(self):
        m1 = await get_mock(1)
        m2 = await get_mock(1)
        self.assertEqual(m1, m2)

