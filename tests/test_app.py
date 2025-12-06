import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    # This must match EXACTLY what your app returns right now
    assert b'CarBazaar' in response.data or b'Welcome' in response.data

def test_greet_route():
    client = app.test_client()
    response = client.get('/greet/Azer')
    assert response.status_code == 200
    assert b'Azer' in response.data

def test_car_detail_route():
    client = app.test_client()
    response = client.get('/car/123')
    assert response.status_code == 200
    assert b'Car #123' in response.data or b'123' in response.data
