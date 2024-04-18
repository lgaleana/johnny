import unittest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app, UrlInput


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hello_world(self):
        mock_response = {'message': 'Hello, Mocked World!'}
        self.client.get = Mock(return_value=Mock(status_code=200, json=lambda: mock_response))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)

    def test_input_url(self):
        mock_url = 'http://mocked.url'
        mock_response = {'message': 'URL received', 'url': mock_url}
        self.client.post = Mock(return_value=Mock(status_code=200, json=lambda: mock_response))
        response = self.client.post('/input_url', json={'url': mock_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)
