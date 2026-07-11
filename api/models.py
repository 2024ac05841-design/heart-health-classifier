"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, Field
from api.constants import HIGH_RISK_PATIENT_EXAMPLE, LOW_RISK_PATIENT_EXAMPLE


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
            "examples": [HIGH_RISK_PATIENT_EXAMPLE, LOW_RISK_PATIENT_EXAMPLE]
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
    ml_model_loaded: bool = Field(
        ..., description="Whether ML model is loaded", example=True
    )
    version: str = Field(..., description="API version", example="1.0.0")


class PredictionRecordDetail(BaseModel):
    """Detailed prediction record for history queries"""

    id: int = Field(..., description="Unique prediction ID", example=1)
    timestamp: str = Field(
        ..., description="ISO format timestamp", example="2026-07-11T10:30:00.123456"
    )
    patient_data: dict = Field(..., description="Input patient features")
    prediction: int = Field(..., description="Prediction class (0 or 1)", example=1)
    prediction_label: str = Field(
        ..., description="Human-readable prediction", example="Disease Present"
    )
    confidence: float = Field(..., description="Model confidence", example=0.85)
    risk_score: float = Field(..., description="Risk probability", example=0.85)
    inference_time_ms: float = Field(
        None, description="Inference time in milliseconds", example=12.5
    )
    preprocessing_time_ms: float = Field(
        None, description="Preprocessing time in milliseconds", example=3.2
    )

    class Config:
        from_attributes = True  # Allows creation from ORM objects


class PredictionHistoryResponse(BaseModel):
    """Statistics summary for prediction history"""

    total_predictions: int = Field(
        ..., description="Total number of predictions", example=1000
    )
    disease_count: int = Field(
        ..., description="Number of disease predictions", example=450
    )
    no_disease_count: int = Field(
        ..., description="Number of no disease predictions", example=550
    )
    avg_risk_score: float = Field(..., description="Average risk score", example=0.52)
    avg_confidence: float = Field(..., description="Average confidence", example=0.78)
    avg_inference_time_ms: float = Field(
        ..., description="Average inference time", example=15.3
    )
    avg_preprocessing_time_ms: float = Field(
        ..., description="Average preprocessing time", example=4.1
    )
