def test_index_route(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"CarBazaar" in response.data


def test_details_not_found(client):
    """Test that non-existent car details return 404."""
    response = client.get('/details/does-not-exist')
    assert response.status_code == 404


def test_login_page_loads(client):
    """Test that the login page loads successfully."""
    response = client.get('/login')
    assert response.status_code == 200


def test_register_page_loads(client):
    """Test that the register page loads successfully."""
    response = client.get('/register')
    assert response.status_code == 200
