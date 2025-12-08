import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app


def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"CarBazaar" in response.data


def test_details_not_found():
    client = app.test_client()
    response = client.get('/details/does-not-exist')
    assert response.status_code == 404
