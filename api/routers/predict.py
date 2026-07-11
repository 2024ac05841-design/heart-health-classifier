"""
Prediction endpoint
"""

from fastapi import APIRouter, HTTPException, status, Depends
import redis
import pandas as pd
import logging
import time
from api.models import PatientData, PredictionResponse, ErrorResponse
from api.dependencies import get_model, get_scaler, get_feature_names
from api.database import get_redis
from api.db_models import PredictionRecord
from api.constants import (
    HIGH_RISK_PREDICTION_EXAMPLE,
    LOW_RISK_PREDICTION_EXAMPLE,
    ERROR_INVALID_INPUT,
    ERROR_PREDICTION_FAILED,
    ERROR_MODEL_NOT_LOADED,
)
from api.monitoring import (
    predictions_counter,
    prediction_confidence_hist,
    prediction_risk_score_hist,
    model_inference_time,
    preprocessing_time,
    feature_value_hist,
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
async def predict(patient: PatientData, db: redis.Redis = Depends(get_redis)):
    """
    **Heart Disease Risk Prediction**

    Submit patient clinical data and receive a prediction on heart disease risk.
    All predictions are automatically saved to Redis for audit and monitoring.

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
    - All predictions are logged to Redis with persistence enabled
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

        # Track feature values for data drift detection
        for feature, value in patient.dict().items():
            feature_value_hist.labels(feature_name=feature).observe(float(value))

        # Ensure correct feature order
        if feature_names:
            input_data = input_data[feature_names]

        # Measure preprocessing time
        preprocess_start = time.time()
        if scaler is not None:
            input_scaled = scaler.transform(input_data)
        else:
            input_scaled = input_data.values
        preprocess_duration = time.time() - preprocess_start
        preprocessing_time.observe(preprocess_duration)

        # Measure model inference time
        inference_start = time.time()
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        inference_duration = time.time() - inference_start
        model_inference_time.observe(inference_duration)

        # Get confidence (probability of predicted class)
        confidence = float(prediction_proba[prediction])

        # Get risk score (probability of disease)
        risk_score = float(prediction_proba[1])

        # Prediction label
        prediction_label = "Disease Present" if prediction == 1 else "No Disease"

        # Determine risk level for metrics
        risk_level = (
            "high" if risk_score > 0.7 else "medium" if risk_score > 0.3 else "low"
        )

        # Record prediction metrics
        predictions_counter.labels(
            prediction_class=prediction_label, risk_level=risk_level
        ).inc()
        prediction_confidence_hist.observe(confidence)
        prediction_risk_score_hist.observe(risk_score)

        # Log prediction with timing
        logger.info(
            f"Prediction: {prediction_label}, Confidence: {confidence:.2f}, "
            f"Risk: {risk_score:.2f}, Inference: {inference_duration*1000:.2f}ms, "
            f"Preprocess: {preprocess_duration*1000:.2f}ms"
        )

        # Save prediction to Redis
        try:
            prediction_record = PredictionRecord(
                patient_data=patient.dict(),
                prediction=int(prediction),
                prediction_label=prediction_label,
                confidence=confidence,
                risk_score=risk_score,
                inference_time_ms=inference_duration * 1000,
                preprocessing_time_ms=preprocess_duration * 1000,
            )
            record_id = prediction_record.save(db)
            logger.info(f"Prediction saved to Redis with ID: {record_id}")
        except Exception as db_error:
            logger.warning(f"Failed to save prediction to Redis: {db_error}")
            # Don't fail the request if database save fails - prediction still succeeds

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
