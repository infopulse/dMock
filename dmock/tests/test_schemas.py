from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock
from dmock.api.schemas import validate_mock_json


class TestMock(test.TestCase):
    mock: Mock

    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    def test_minimum_new_mock(self):
        payload = {
            "name": "test",
        }
        self.assertTrue(validate_mock_json(payload)['valid'])

    def test_minimum_new_mock_negative_1(self):
        payload = {
            "name1": "test",
        }
        self.assertFalse(validate_mock_json(payload)['valid'])

    def test_minimum_new_mock_negative_2(self):
        payload = {
            "name": ["test"],
        }
        self.assertFalse(validate_mock_json(payload)['valid'])\

    def test_complete_new_mock(self):
        payload = {
            "name": "test",
            "status": "draft",
            "labels": ["label1", "label2"],
            "delay": 0,
            "isDefault": False,
            "priority": 1,
            "method": "GET",
            "url": "http://localhost",
            "responseHeaders": {"header1": "value1"},
            "responseBody": "body",
            "statusCode": 200,
            "isAction": False,
            "action": "",
        }
        self.assertTrue(validate_mock_json(payload)['valid'])

    def test_more_fields_new_mock(self):
        payload = {
            "name": "test",
            "status": "draft",
            "labels": ["label1", "label2"],
            "delay": 0,
            "isDefault": False,
            "priority": 1,
            "method": "GET",
            "url": "http://localhost",
            "responseHeaders": {"header1": "value1"},
            "responseBody": "body",
            "statusCode": 200,
            "isAction": False,
            "action": "",
            "extra": "extra"
        }
        self.assertTrue(validate_mock_json(payload)['valid'])