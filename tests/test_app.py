import sys
import os

# Add the 'src' directory to the Python path — this is exactly what the PDF shows
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now we can import the 'app' object
from app import app

def test_index_route():
    """Tests the '/' route to ensure it returns 'Hello, World!'."""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Welcome to CarBazaar – Buy & Sell Cars in Azerbaijan!'

def test_greet_route():
    """Tests the '/greet/<name>' route with a sample name."""
    client = app.test_client()
    response = client.get('/greet/TestUser')
    assert response.status_code == 200
    assert b'Hello, TestUser!' in response.data

def test_car_detail_route():
    """Test the car detail route."""
    client = app.test_client()
    response = client.get('/car/123')
    assert response.status_code == 200
    assert b'Car #123' in response.data
