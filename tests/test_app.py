import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_greet_route():
    client = app.test_client()
    response = client.get('/greet/TestUser')
    assert response.status_code == 200
    assert b'Hello, TestUser!' in response.data
