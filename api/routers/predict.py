"""
Prediction endpoint
"""

from fastapi import APIRouter, HTTPException, status
import pandas as pd
import logging
from api.models import PatientData, PredictionResponse, ErrorResponse
from api.dependencies import get_model, get_scaler, get_feature_names
from api.constants import (
    HIGH_RISK_PREDICTION_EXAMPLE,
    LOW_RISK_PREDICTION_EXAMPLE,
    ERROR_INVALID_INPUT,
    ERROR_PREDICTION_FAILED,
    ERROR_MODEL_NOT_LOADED,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
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
                        "high_risk": HIGH_RISK_PREDICTION_EXAMPLE,
                        "low_risk": LOW_RISK_PREDICTION_EXAMPLE,
                    }
                }
            },
        },
        400: {
            "description": "Invalid input data",
            "model": ErrorResponse,
            "content": {"application/json": {"example": ERROR_INVALID_INPUT}},
        },
        500: {
            "description": "Prediction failed due to server error",
            "model": ErrorResponse,
            "content": {"application/json": {"example": ERROR_PREDICTION_FAILED}},
        },
        503: {
            "description": "Model not loaded or unavailable",
            "model": ErrorResponse,
            "content": {"application/json": {"example": ERROR_MODEL_NOT_LOADED}},
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
    model = get_model()
    scaler = get_scaler()
    feature_names = get_feature_names()

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
