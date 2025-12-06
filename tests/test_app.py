import sys
import os
import pytest

# Fixture to set PYTHONPATH for all tests (fixes CI path issues)
@pytest.fixture(autouse=True)
def add_src_to_path():
    # Get project root (where tests/ is)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Add src to path
    sys.path.insert(0, os.path.join(project_root, 'src'))
    yield
    # Clean up after test
    sys.path.pop(0)

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
