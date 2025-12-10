import pytest
import sys
import os

# Ensure project root is on path so `src` is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app, db

@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # Create all tables
            db.create_all()
        yield client
        with app.app_context():
            # Clean up after tests
            db.drop_all()

@pytest.fixture
def app_context():
    """Provide an application context for tests that need it."""
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
