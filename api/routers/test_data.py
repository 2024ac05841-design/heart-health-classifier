"""
Test data generation endpoint
"""

from fastapi import APIRouter, Query
import numpy as np
from typing import Dict
import logging
from api.models import PatientData

router = APIRouter()
logger = logging.getLogger(__name__)


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


@router.get(
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
    sample_data = generate_sample_patient_data(risk_level)
    logger.info(f"Generated test data with risk_level={risk_level}")
    return PatientData(**sample_data)
