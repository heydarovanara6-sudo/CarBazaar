import pytest
import sys
from pathlib import Path

# Add the project root directory to Python path
# This works both locally and in GitHub Actions
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Now we can import app
from app import app


def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"CarBazaar" in response.data


def test_greet_route():
    client = app.test_client()
    response = client.get("/greet/Azer")
    assert response.status_code == 200
    assert b"Hello, Azer!" in response.data


def test_car_detail_route():
    client = app.test_client()
    response = client.get("/car/777")
    assert response.status_code == 200
    assert b"Car #777" in response.data
