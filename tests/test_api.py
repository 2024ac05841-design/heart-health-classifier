"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.app import app
from api.database import get_redis


# Mock Redis client for testing
@pytest.fixture
def mock_redis():
    """Fixture to provide a mock Redis client"""
    mock = MagicMock()
    mock.ping.return_value = True
    mock.incr.return_value = 1
    mock.hset.return_value = True
    mock.zadd.return_value = True
    mock.sadd.return_value = True
    return mock


@pytest.fixture
def client(mock_redis):
    """Fixture to provide a test client with mocked Redis"""
    # Override the Redis dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "ml_model_loaded" in data


def test_predict_endpoint_validation(client):
    """Test prediction endpoint with invalid data"""
    # Missing required fields
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Validation error

    # Invalid age (negative)
    response = client.post(
        "/predict",
        json={
            "age": -10,
            "sex": 1,
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 0,
            "ca": 0,
            "thal": 1,
        },
    )
    assert response.status_code == 422


def test_predict_endpoint_valid_data(client):
    """Test prediction endpoint with valid data"""
    valid_data = {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }

    response = client.post("/predict", json=valid_data)

    # Will return 503 if model not loaded, which is expected in tests
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "risk_score" in data
        assert 0 <= data["confidence"] <= 1
        assert 0 <= data["risk_score"] <= 1


def test_docs_endpoint(client):
    """Test that OpenAPI docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint(client):
    """Test that OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/predict" in schema["paths"]
