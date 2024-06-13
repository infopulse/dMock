from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.models.models import Mock, Rule, MockLog, Settings
from fastapi.testclient import TestClient
from dmock.main import app
from dmock.models.setup import set_data


class TestMock(test.TestCase):
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')
        self.client = TestClient(app)

    def tearDown(self):
        finalizer()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        await set_data()

    async def test_init_setup_works(self):
        mock = await Mock.get(id=1)
        self.assertEqual(mock.id, 1)

    async def test__create_mock_api(self):
        request = {
            "name": "GET-MOCK-01",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "GET",
            "url": "/aaa",
            "responseHeaders": {
                "Content-Type": "text/plain"
            },
            "responseBody": "hello world",
            "statusCode": 201
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 201)
        mock = await Mock.get(id=response.json()['id'])
        self.assertEqual(mock.name, "GET-MOCK-01")

    async def test__create_mock_api_json(self):
        request = {
            "name": "GET-MOCK-02",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "GET",
            "url": "/aaa",
            "responseHeaders": {
                "Content-Type": "application/json"
            },
            "responseBody": "{\"helloWorld\":\"some string\"}",
            "statusCode": 201
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json()['responseBody']), dict)
        mock = await Mock.get(id=response.json()['id'])
        self.assertEqual(mock.name, "GET-MOCK-02")

    async def test__create_mock_api_xml(self):
        request_body = """
        <?xmlversion=\"1.0\"encoding=\"UTF-8\"?><soap:Envelopexmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
        <soap:Header/><soap:Body><GetUserDetailsResponsexmlns=\"http://example.com/webservices\"><GetUserDetailsResult>
        <User><UserID>12345</UserID><FirstName>John</FirstName><LastName>Doe</LastName><Email>john.doe@example.com</Email>
        <PhoneNumber>+1234567890</PhoneNumber></User></GetUserDetailsResult></GetUserDetailsResponse>
        </soap:Body></soap:Envelope>
        """
        request = {
            "name": "GET-MOCK-03",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "GET",
            "url": "/aaa",
            "responseHeaders": {
                "Content-Type": "application/xml"
            },
            "responseBody": request_body,
            "statusCode": 201,
            "isAction": False,
            "rules": [
                {
                    "type": "2-url",
                    "operation": "contains",
                    "key": "xml",
                    "isActive": True
                }

            ]
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 201)
        mock = await Mock.get(id=response.json()['id'])
        self.assertEqual(mock.name, "GET-MOCK-03")

    async def test__create_mock_api_post(self):
        request = {
            "name": "GET-MOCK-04",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "POST",
            "url": "/post",
            "responseHeaders": None,
            "responseBody": None,
            "statusCode": 201
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 201)
        mock = await Mock.get(id=response.json()['id'])
        self.assertEqual(mock.name, "GET-MOCK-04")

    async def test__create_mock_api_patch(self):
        request = {
            "name": "GET-MOCK-05",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "PATCH",
            "url": "/post",
            "responseHeaders": None,
            "responseBody": None,
            "statusCode": 201
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 201)
        mock = await Mock.get(id=response.json()['id'])
        self.assertEqual(mock.name, "GET-MOCK-05")

    async def test__create_mock_api_invalid_method(self):
        request = {
            "name": "GET-MOCK-05",
            "status": "draft",
            "labels": [
                "test", "first"
            ],
            "delay": 0,
            "method": "TEST",
            "url": "/post",
            "responseHeaders": None,
            "responseBody": None,
            "statusCode": 201
        }

        response = self.client.post('/api/mocks', json=request)
        self.assertEqual(response.status_code, 422)
