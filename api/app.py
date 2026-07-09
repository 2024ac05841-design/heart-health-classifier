"""
FastAPI application for Heart Disease prediction
"""

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from typing import Dict
import logging
from prometheus_fastapi_instrumentator import Instrumentator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with enhanced metadata
app = FastAPI(
    title="Heart Disease Prediction API",
    description="""
## 🫀 Heart Disease Prediction MLOps API

This API provides machine learning-powered predictions for heart disease risk assessment.

### Features
* **Real-time Predictions**: Get instant heart disease risk predictions
* **Model Information**: Access trained model metadata and configuration
* **Health Monitoring**: Built-in health checks and Prometheus metrics
* **Interactive Documentation**: Full Swagger/OpenAPI documentation

### Dataset
Based on the UCI Heart Disease dataset with 13 clinical features.

### Model Performance
The model achieves high accuracy on the validation set and uses ensemble methods for robust predictions.
    """,
    version="1.0.0",
    contact={
        "name": "MLOps Team",
        "url": "https://github.com/2024ac05841-design/heart-health-classifier",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url=None,  # Disabled - using only Swagger UI
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app)


# API Tags for Swagger grouping
tags_metadata = [
    {
        "name": "Health",
        "description": "Health check and status endpoints for monitoring service availability.",
    },
    {
        "name": "Prediction",
        "description": "Machine learning prediction endpoints for heart disease risk assessment.",
    },
    {
        "name": "Model",
        "description": "Model information and metadata endpoints.",
    },
    {
        "name": "Testing",
        "description": "Test data generation utilities for API testing and development.",
    },
]


class PatientData(BaseModel):
    """Input data model for heart disease prediction"""

    age: float = Field(
        ..., description="Patient age in years", ge=0, le=120, example=63
    )
    sex: float = Field(
        ..., description="Biological sex (1=male, 0=female)", ge=0, le=1, example=1
    )
    cp: float = Field(
        ...,
        description="Chest pain type (0=typical angina, 1=atypical angina, 2=non-anginal pain, 3=asymptomatic)",
        ge=0,
        le=3,
        example=3,
    )
    trestbps: float = Field(
        ..., description="Resting blood pressure in mm Hg", ge=0, example=145
    )
    chol: float = Field(
        ..., description="Serum cholesterol in mg/dl", ge=0, example=233
    )
    fbs: float = Field(
        ...,
        description="Fasting blood sugar > 120 mg/dl (1=true, 0=false)",
        ge=0,
        le=1,
        example=1,
    )
    restecg: float = Field(
        ...,
        description="Resting electrocardiographic results (0=normal, 1=ST-T wave abnormality, 2=left ventricular hypertrophy)",
        ge=0,
        le=2,
        example=0,
    )
    thalach: float = Field(
        ...,
        description="Maximum heart rate achieved during exercise",
        ge=0,
        example=150,
    )
    exang: float = Field(
        ..., description="Exercise induced angina (1=yes, 0=no)", ge=0, le=1, example=0
    )
    oldpeak: float = Field(
        ...,
        description="ST depression induced by exercise relative to rest",
        ge=0,
        example=2.3,
    )
    slope: float = Field(
        ...,
        description="Slope of the peak exercise ST segment (0=upsloping, 1=flat, 2=downsloping)",
        ge=0,
        le=2,
        example=0,
    )
    ca: float = Field(
        ...,
        description="Number of major vessels colored by fluoroscopy (0-3)",
        ge=0,
        le=3,
        example=0,
    )
    thal: float = Field(
        ...,
        description="Thalassemia (0=normal, 1=fixed defect, 2=reversible defect)",
        ge=0,
        le=2,
        example=1,
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
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
                },
                {
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
                },
            ]
        }


class PredictionResponse(BaseModel):
    """Response model for heart disease prediction"""

    prediction: int = Field(
        ..., description="Prediction class (0=No disease, 1=Disease present)", example=1
    )
    prediction_label: str = Field(
        ..., description="Human-readable prediction label", example="Disease Present"
    )
    confidence: float = Field(
        ...,
        description="Confidence score of the prediction (0.0-1.0)",
        ge=0,
        le=1,
        example=0.85,
    )
    risk_score: float = Field(
        ...,
        description="Probability of heart disease presence (0.0-1.0)",
        ge=0,
        le=1,
        example=0.85,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1,
                "prediction_label": "Disease Present",
                "confidence": 0.85,
                "risk_score": 0.85,
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""

    detail: str = Field(..., description="Error message", example="Model not loaded")


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str = Field(..., description="Service status", example="healthy")
    model_loaded: bool = Field(
        ..., description="Whether ML model is loaded", example=True
    )
    version: str = Field(..., description="API version", example="1.0.0")


# Load model and artifacts at startup
model = None
scaler = None
feature_names = None


@app.on_event("startup")
async def load_model():
    """Load model and preprocessing artifacts"""
    global model, scaler, feature_names

    try:
        model = joblib.load("models/best_model.pkl")
        scaler = joblib.load("models/scaler.pkl")

        # Load feature names if available
        try:
            import json

            with open("models/feature_names.json", "r") as f:
                feature_names = json.load(f)["features"]
        except:
            feature_names = None

        logger.info("✓ Model and artifacts loaded successfully")
        logger.info("=" * 80)
        logger.info("🫀 Heart Disease Prediction API is ready!")
        logger.info("=" * 80)
        logger.info("📚 Interactive API Documentation (Swagger UI):")
        logger.info("   • http://localhost:8000/docs")
        logger.info("")
        logger.info("🧪 Testing the API:")
        logger.info("   1. Visit the Swagger UI at /docs")
        logger.info(
            "   2. Try the /generate-test-data endpoint to create sample patient data"
        )
        logger.info("   3. Copy the generated data and use it in the /predict endpoint")
        logger.info("")
        logger.info("🔍 Available Endpoints:")
        logger.info("   • GET  /health              - Health check")
        logger.info("   • POST /predict             - Heart disease prediction")
        logger.info("   • GET  /model/info          - Model information")
        logger.info("   • GET  /generate-test-data  - Generate sample test data")
        logger.info("   • GET  /metrics             - Prometheus metrics")
        logger.info("=" * 80)
    except Exception as e:
        logger.error(f"✗ Error loading model: {e}")
        logger.warning("Model not loaded - predictions will fail")
        logger.info("=" * 80)


@app.get(
    "/",
    summary="Root endpoint",
    description="Returns API information and available endpoints",
    tags=["Health"],
)
async def root():
    """
    **Root Endpoint**

    Provides basic API information and lists all available endpoints.
    """
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model/info",
            "generate_test_data": "/generate-test-data",
            "docs": "/docs",
            "metrics": "/metrics",
        },
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API and model availability",
    tags=["Health"],
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "model_loaded": True,
                        "version": "1.0.0",
                    }
                }
            },
        }
    },
)
async def health_check():
    """
    **Health Check Endpoint**

    Returns the current health status of the service, including:
    - Service status (healthy/degraded)
    - Model loading status
    - API version

    Used by Kubernetes liveness and readiness probes.
    """
    model_loaded = model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "version": "1.0.0",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict heart disease risk",
    description="Submit patient data and receive heart disease risk prediction",
    tags=["Prediction"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "examples": {
                        "high_risk": {
                            "summary": "High risk result",
                            "description": "Patient with high probability of heart disease",
                            "value": {
                                "prediction": 1,
                                "prediction_label": "Disease Present",
                                "confidence": 0.85,
                                "risk_score": 0.85,
                            },
                        },
                        "low_risk": {
                            "summary": "Low risk result",
                            "description": "Patient with low probability of heart disease",
                            "value": {
                                "prediction": 0,
                                "prediction_label": "No Disease",
                                "confidence": 0.92,
                                "risk_score": 0.08,
                            },
                        },
                    }
                }
            },
        },
        400: {
            "description": "Invalid input data",
            "model": ErrorResponse,
            "content": {
                "application/json": {"example": {"detail": "Invalid feature values"}}
            },
        },
        500: {
            "description": "Prediction failed due to server error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "Prediction failed: Internal server error"}
                }
            },
        },
        503: {
            "description": "Model not loaded or unavailable",
            "model": ErrorResponse,
            "content": {
                "application/json": {"example": {"detail": "Model not loaded"}}
            },
        },
    },
)
async def predict(patient: PatientData):
    """
    **Heart Disease Risk Prediction**

    Submit patient clinical data and receive a prediction on heart disease risk.

    ### Input Features
    The model requires 13 clinical features:
    - **Demographics**: age, sex
    - **Cardiovascular**: chest pain type, blood pressure, cholesterol, ECG results
    - **Exercise**: max heart rate, exercise-induced angina, ST depression
    - **Medical tests**: thalassemia, number of major vessels

    ### Output
    Returns:
    - **prediction**: Binary classification (0=No disease, 1=Disease present)
    - **prediction_label**: Human-readable prediction
    - **confidence**: Model confidence in the prediction (0.0-1.0)
    - **risk_score**: Probability of heart disease presence (0.0-1.0)

    ### Model Information
    - Trained on UCI Heart Disease dataset
    - Uses ensemble methods (Random Forest/Logistic Regression)
    - Features are automatically scaled using saved scaler
    """
    if model is None:
        logger.error("Model not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded"
        )

    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([patient.dict()])

        # Ensure correct feature order
        if feature_names:
            input_data = input_data[feature_names]

        # Scale features
        if scaler is not None:
            input_scaled = scaler.transform(input_data)
        else:
            input_scaled = input_data.values

        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]

        # Get confidence (probability of predicted class)
        confidence = float(prediction_proba[prediction])

        # Get risk score (probability of disease)
        risk_score = float(prediction_proba[1])

        # Prediction label
        prediction_label = "Disease Present" if prediction == 1 else "No Disease"

        # Log prediction
        logger.info(
            f"Prediction: {prediction_label}, Confidence: {confidence:.2f}, Risk: {risk_score:.2f}"
        )

        return PredictionResponse(
            prediction=int(prediction),
            prediction_label=prediction_label,
            confidence=confidence,
            risk_score=risk_score,
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


@app.get(
    "/model/info",
    summary="Get model information",
    description="Retrieve metadata about the trained machine learning model",
    tags=["Model"],
    responses={
        200: {
            "description": "Model information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "model_type": "RandomForestClassifier",
                        "features": [
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
                        ],
                        "n_features": 13,
                        "scaler_loaded": True,
                    }
                }
            },
        },
        503: {
            "description": "Model not loaded",
            "model": ErrorResponse,
            "content": {
                "application/json": {"example": {"detail": "Model not loaded"}}
            },
        },
    },
)
async def model_info():
    """
    **Model Information Endpoint**

    Returns metadata about the loaded machine learning model:
    - Model type (e.g., RandomForestClassifier, LogisticRegression)
    - Feature names and count
    - Scaler status
    - Additional model-specific parameters

    This endpoint is useful for understanding the model configuration and verifying correct loading.
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded"
        )

    info = {
        "model_type": type(model).__name__,
        "features": feature_names if feature_names else "Unknown",
        "scaler_loaded": scaler is not None,
    }

    # Add model-specific info
    if hasattr(model, "n_features_in_"):
        info["n_features"] = model.n_features_in_

    return info


def generate_sample_patient_data(risk_level: str = "random") -> Dict:
    """
    Generate synthetic patient data for testing

    Args:
        risk_level: 'low', 'high', or 'random'

    Returns:
        Dictionary with patient data
    """
    np.random.seed()  # Use different seed each time

    if risk_level == "high":
        # Generate high-risk patient profile
        return {
            "age": float(np.random.randint(60, 78)),
            "sex": float(np.random.choice([0, 1])),
            "cp": float(np.random.randint(2, 4)),  # Higher chest pain type
            "trestbps": float(np.random.randint(140, 200)),  # Higher blood pressure
            "chol": float(np.random.randint(240, 400)),  # Higher cholesterol
            "fbs": float(np.random.choice([0, 1])),
            "restecg": float(np.random.randint(0, 3)),
            "thalach": float(np.random.randint(100, 140)),  # Lower max heart rate
            "exang": float(np.random.choice([0, 1])),
            "oldpeak": float(
                np.round(np.random.uniform(1.5, 5.0), 1)
            ),  # Higher ST depression
            "slope": float(np.random.randint(0, 3)),
            "ca": float(np.random.randint(1, 4)),  # More vessels
            "thal": float(np.random.randint(1, 3)),  # Fixed or reversible defect
        }
    elif risk_level == "low":
        # Generate low-risk patient profile
        return {
            "age": float(np.random.randint(29, 50)),
            "sex": float(np.random.choice([0, 1])),
            "cp": float(np.random.randint(0, 2)),  # Lower chest pain type
            "trestbps": float(np.random.randint(100, 130)),  # Normal blood pressure
            "chol": float(np.random.randint(150, 220)),  # Normal cholesterol
            "fbs": float(0),  # Normal fasting blood sugar
            "restecg": float(0),  # Normal ECG
            "thalach": float(np.random.randint(150, 200)),  # Higher max heart rate
            "exang": float(0),  # No exercise-induced angina
            "oldpeak": float(
                np.round(np.random.uniform(0, 1.0), 1)
            ),  # Lower ST depression
            "slope": float(np.random.randint(0, 2)),
            "ca": float(0),  # No vessels colored
            "thal": float(0),  # Normal thalassemia
        }
    else:
        # Generate random patient profile
        return {
            "age": float(np.random.randint(29, 78)),
            "sex": float(np.random.randint(0, 2)),
            "cp": float(np.random.randint(0, 4)),
            "trestbps": float(np.random.randint(94, 200)),
            "chol": float(np.random.randint(126, 400)),
            "fbs": float(np.random.randint(0, 2)),
            "restecg": float(np.random.randint(0, 3)),
            "thalach": float(np.random.randint(71, 202)),
            "exang": float(np.random.randint(0, 2)),
            "oldpeak": float(np.round(np.random.uniform(0, 6.2), 1)),
            "slope": float(np.random.randint(0, 3)),
            "ca": float(np.random.randint(0, 4)),
            "thal": float(np.random.randint(0, 3)),
        }


@app.get(
    "/generate-test-data",
    response_model=PatientData,
    summary="Generate test patient data",
    description="Generate synthetic patient data for testing the prediction endpoint",
    tags=["Testing"],
    responses={
        200: {
            "description": "Test data generated successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "random": {
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
                        },
                        "high_risk": {
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
                        },
                        "low_risk": {
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
                        },
                    }
                }
            },
        }
    },
)
async def generate_test_data(
    risk_level: str = Query(
        default="random",
        description="Risk level for generated data: 'low', 'high', or 'random'",
        pattern="^(low|high|random)$",
    )
):
    """
    **Generate Test Patient Data**

    Generates synthetic patient data for testing the prediction endpoint.
    This is useful for:
    - Testing the API without manual data entry
    - Demonstrating the prediction endpoint
    - Automated testing and validation
    - Understanding feature ranges

    ### Risk Levels
    - **low**: Generates a patient profile with lower risk factors (younger age, normal vitals, no concerning symptoms)
    - **high**: Generates a patient profile with higher risk factors (older age, elevated vitals, concerning symptoms)
    - **random**: Generates a patient profile with random values across all features

    ### Usage
    1. Call this endpoint to get sample patient data
    2. Copy the returned JSON
    3. Use it as input for the `/predict` endpoint

    ### Note
    This generates **synthetic data** for testing purposes only. It should not be used for actual medical diagnosis.
    """
    try:
        sample_data = generate_sample_patient_data(risk_level)
        logger.info(f"Generated test data with risk_level={risk_level}")
        return PatientData(**sample_data)
    except Exception as e:
        logger.error(f"Error generating test data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate test data: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
