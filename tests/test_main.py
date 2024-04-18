import unittest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app, UrlInput, scrape_url, extract_info_with_chatgpt, split_html_content
import os


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template.name, 'index.html')
        self.assertIsInstance(response.context, dict)
        self.assertIn('request', response.context)

    def test_input_url(self):
        mock_url = 'http://mocked.url'
        mock_extracted_info = 'Mocked extracted info'
        mock_response = {'message': 'URL received', 'url': mock_url, 'extracted_info': mock_extracted_info}
        self.client.post = Mock(return_value=Mock(status_code=200, json=lambda: mock_response))
        response = self.client.post('/input_url', json={'url': mock_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)

    def test_scrape_url(self):
        mock_url = 'http://mocked.url'
        mock_html_content = '<html><body>Mocked HTML content</body></html>'
        scrape_url = Mock(return_value=mock_html_content)
        self.assertEqual(scrape_url(mock_url), mock_html_content)

    def test_split_html_content(self):
        mock_html_content = 'a' * 900000
        expected_result = ['a' * 300000, 'a' * 300000, 'a' * 300000]
        self.assertEqual(split_html_content(mock_html_content), expected_result)

    def test_extract_info_with_chatgpt(self):
        mock_html_content_list = ['<html><body>Mocked HTML content</body></html>', '<html><body>Another mocked HTML content</body></html>']
        mock_extracted_info = 'Mocked extracted info'
        extract_info_with_chatgpt = Mock(return_value=mock_extracted_info)
        self.assertEqual(extract_info_with_chatgpt(mock_html_content_list), mock_extracted_info)
