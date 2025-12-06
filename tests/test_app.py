import pytest
from src.app import app   # ← This is the correct, clean import

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
    response = client.get("/car/123")
    assert response.status_code == 200
    assert b"Car #123" in response.data
