import sys
import os

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now we can import the 'app' object from our source code
from app import app

def test_index_route():
    """Tests the '/' route to ensure it returns 'Welcome to CarBazaar...'."""
    # Create a test client using the Flask application context
    client = app.test_client()
    # Use the client to make a GET request to the index route
    response = client.get('/')
    # Assert that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response data is the expected string
    assert response.data == b'Welcome to CarBazaar – Buy & Sell Cars in Azerbaijan!'

def test_greet_route():
    """Tests the '/greet/<name>' route with a sample name."""
    client = app.test_client()
    # Make a GET request to the dynamic greet route
    response = client.get('/greet/TestUser')
    assert response.status_code == 200
    # Check that the personalized greeting is in the response data
    assert b'Hello, TestUser!' in response.data

def test_car_detail_route():
    """Tests the '/car/<int:car_id>' route."""
    client = app.test_client()
    response = client.get('/car/123')
    assert response.status_code == 200
    assert b'Car #123' in response.data
