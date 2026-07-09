"""
FastAPI application for Heart Disease prediction
"""

from fastapi import FastAPI, HTTPException
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

# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="ML model for predicting heart disease risk",
    version="1.0.0",
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


class PatientData(BaseModel):
    """Input data model for prediction"""

    age: float = Field(..., description="Age in years", ge=0, le=120)
    sex: float = Field(..., description="Sex (1=male, 0=female)")
    cp: float = Field(..., description="Chest pain type (0-3)")
    trestbps: float = Field(..., description="Resting blood pressure (mm Hg)", ge=0)
    chol: float = Field(..., description="Serum cholesterol (mg/dl)", ge=0)
    fbs: float = Field(
        ..., description="Fasting blood sugar > 120 mg/dl (1=true, 0=false)"
    )
    restecg: float = Field(..., description="Resting ECG results (0-2)")
    thalach: float = Field(..., description="Maximum heart rate achieved", ge=0)
    exang: float = Field(..., description="Exercise induced angina (1=yes, 0=no)")
    oldpeak: float = Field(..., description="ST depression induced by exercise", ge=0)
    slope: float = Field(..., description="Slope of peak exercise ST segment (0-2)")
    ca: float = Field(..., description="Number of major vessels (0-3)")
    thal: float = Field(
        ..., description="Thalassemia (0=normal, 1=fixed defect, 2=reversable defect)"
    )

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Response model for prediction"""

    prediction: int
    prediction_label: str
    confidence: float
    risk_score: float


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

        logger.info("Model and artifacts loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.warning("Model not loaded - predictions will fail")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
            "metrics": "/metrics",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "version": "1.0.0",
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(patient: PatientData):
    """
    Predict heart disease risk

    Args:
        patient: Patient data including all required features

    Returns:
        Prediction result with confidence score
    """
    if model is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded")

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
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/model/info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    info = {
        "model_type": type(model).__name__,
        "features": feature_names if feature_names else "Unknown",
        "scaler_loaded": scaler is not None,
    }

    # Add model-specific info
    if hasattr(model, "n_features_in_"):
        info["n_features"] = model.n_features_in_

    return info


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
