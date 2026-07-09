"""
Constants for API responses and examples

This module centralizes all response examples, error messages, and constant values
used across the API for consistency and maintainability.
"""

# Feature names in order
FEATURE_NAMES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

# =============================================================================
# Patient Data Examples
# =============================================================================

HIGH_RISK_PATIENT_EXAMPLE = {
    "name": "High Risk Patient",
    "summary": "Patient with high heart disease risk",
    "description": "Example of a patient profile indicating higher likelihood of heart disease",
    "value": {
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
    },
}

LOW_RISK_PATIENT_EXAMPLE = {
    "name": "Low Risk Patient",
    "summary": "Patient with low heart disease risk",
    "description": "Example of a patient profile indicating lower likelihood of heart disease",
    "value": {
        "age": 45,
        "sex": 0,
        "cp": 0,
        "trestbps": 120,
        "chol": 180,
        "fbs": 0,
        "restecg": 0,
        "thalach": 170,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 1,
        "ca": 0,
        "thal": 0,
    },
}

# =============================================================================
# Prediction Response Examples
# =============================================================================

HIGH_RISK_PREDICTION_EXAMPLE = {
    "summary": "High risk result",
    "description": "Patient with high probability of heart disease",
    "value": {
        "prediction": 1,
        "prediction_label": "Disease Present",
        "confidence": 0.85,
        "risk_score": 0.85,
    },
}

LOW_RISK_PREDICTION_EXAMPLE = {
    "summary": "Low risk result",
    "description": "Patient with low probability of heart disease",
    "value": {
        "prediction": 0,
        "prediction_label": "No Disease",
        "confidence": 0.92,
        "risk_score": 0.08,
    },
}

# =============================================================================
# Test Data Generation Examples
# =============================================================================

RANDOM_TEST_DATA_EXAMPLE = {
    "summary": "Random patient data",
    "description": "Randomly generated patient with mixed risk factors",
    "value": {
        "age": 55,
        "sex": 1,
        "cp": 2,
        "trestbps": 140,
        "chol": 250,
        "fbs": 1,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 1,
        "ca": 1,
        "thal": 1,
    },
}

HIGH_RISK_TEST_DATA_EXAMPLE = {
    "summary": "High risk patient data",
    "description": "Generated patient with high-risk profile",
    "value": {
        "age": 68,
        "sex": 1,
        "cp": 3,
        "trestbps": 165,
        "chol": 320,
        "fbs": 1,
        "restecg": 2,
        "thalach": 120,
        "exang": 1,
        "oldpeak": 3.5,
        "slope": 2,
        "ca": 2,
        "thal": 2,
    },
}

LOW_RISK_TEST_DATA_EXAMPLE = {
    "summary": "Low risk patient data",
    "description": "Generated patient with low-risk profile",
    "value": {
        "age": 42,
        "sex": 0,
        "cp": 0,
        "trestbps": 118,
        "chol": 185,
        "fbs": 0,
        "restecg": 0,
        "thalach": 175,
        "exang": 0,
        "oldpeak": 0.3,
        "slope": 1,
        "ca": 0,
        "thal": 0,
    },
}

# =============================================================================
# Model Info Response Example
# =============================================================================

MODEL_INFO_EXAMPLE = {
    "model_type": "RandomForestClassifier",
    "features": FEATURE_NAMES,
    "n_features": 13,
    "scaler_loaded": True,
}

# =============================================================================
# Error Response Examples
# =============================================================================

ERROR_MODEL_NOT_LOADED = {"detail": "Model not loaded"}
ERROR_INVALID_INPUT = {"detail": "Invalid feature values"}
ERROR_PREDICTION_FAILED = {"detail": "Prediction failed: Internal server error"}

# =============================================================================
# API Information
# =============================================================================

API_VERSION = "1.0.0"
API_ENDPOINTS = {
    "health": "/health",
    "predict": "/predict",
    "model_info": "/model/info",
    "generate_test_data": "/generate-test-data",
    "docs": "/docs",
    "metrics": "/metrics",
}
