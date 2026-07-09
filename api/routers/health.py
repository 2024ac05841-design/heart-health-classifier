"""
Health and status endpoints
"""

from fastapi import APIRouter
from api.models import HealthResponse
from api.dependencies import get_model

router = APIRouter()


@router.get(
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


@router.get(
    "/health",
    response_model=HealthResponse,
    include_in_schema=False,  # Hide from Swagger UI, but keep for K8s probes
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
    model = get_model()
    model_loaded = model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "version": "1.0.0",
    }
