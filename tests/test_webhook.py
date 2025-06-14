import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Code Review Bot" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    # This might fail if GitHub token is not set
    response = client.get("/health")
    # Just check that endpoint exists
    assert response.status_code in [200, 503]
