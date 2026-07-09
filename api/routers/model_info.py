"""
Model information endpoint
"""

from fastapi import APIRouter, HTTPException, status
from api.models import ErrorResponse
from api.dependencies import get_model, get_scaler, get_feature_names
from api.constants import MODEL_INFO_EXAMPLE, ERROR_MODEL_NOT_LOADED

router = APIRouter()


@router.get(
    "/model/info",
    summary="Get model information",
    description="Retrieve metadata about the trained machine learning model",
    tags=["Model"],
    responses={
        200: {
            "description": "Model information retrieved successfully",
            "content": {"application/json": {"example": MODEL_INFO_EXAMPLE}},
        },
        503: {
            "description": "Model not loaded",
            "model": ErrorResponse,
            "content": {"application/json": {"example": ERROR_MODEL_NOT_LOADED}},
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
    model = get_model()
    scaler = get_scaler()
    feature_names = get_feature_names()

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
