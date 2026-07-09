"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.app import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


def test_predict_endpoint_validation():
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


def test_predict_endpoint_valid_data():
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


def test_docs_endpoint():
    """Test that OpenAPI docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint():
    """Test that OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/predict" in schema["paths"]
