from fastapi.testclient import TestClient
from main import app
import pytest
from unittest.mock import Mock

def test_hello_world(mocker):
    mock_response = {'message': 'Hello, Mocked World!'}
    mocker.patch.object(TestClient, 'get', return_value=Mock(status_code=200, json=lambda: mock_response))
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == mock_response
