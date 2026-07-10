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
