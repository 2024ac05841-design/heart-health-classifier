"""
Health and status endpoints
"""

from fastapi import APIRouter
from api.models import HealthResponse
from api.dependencies import get_model
from api.constants import API_VERSION, API_ENDPOINTS

router = APIRouter()


@router.get(
    "/",
    summary="Root endpoint",
    description="Returns API information and available endpoints",
    tags=["Health"],
    include_in_schema=False,  # Hide from Swagger UI
)
async def root():
    """
    **Root Endpoint**

    Provides basic API information and lists all available endpoints.
    """
    return {
        "message": "Heart Disease Prediction API",
        "version": API_VERSION,
        "status": "running",
        "endpoints": API_ENDPOINTS,
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
        "version": API_VERSION,
    }
