import sys
import os

# Add src to path (matches PDF)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

def test_index_route():
    """Test home route."""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'CarBazaar' in response.data

def test_greet_route():
    """Test greet route."""
    client = app.test_client()
    response = client.get('/greet/Buyer')
    assert response.status_code == 200
    assert b'Hello, Buyer!' in response.data

def test_car_detail_route():
    """Test car detail route."""
    client = app.test_client()
    response = client.get('/car/123')
    assert response.status_code == 200
    assert b'Car #123' in response.data
