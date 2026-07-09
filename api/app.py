"""
FastAPI application for Heart Disease prediction

Modular structure:
- models.py: Pydantic request/response models
- dependencies.py: Model loading and dependency injection
- routers/: Endpoint routers organized by functionality
  - health.py: Health check and status endpoints
  - predict.py: Prediction endpoint
  - model_info.py: Model information endpoint
  - test_data.py: Test data generation endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import logging

# Import routers
from api.routers import health, predict, model_info, test_data
from api.dependencies import load_model_artifacts

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

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, tags=["Prediction"])
app.include_router(model_info.router, tags=["Model"])
app.include_router(test_data.router, tags=["Testing"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application and load ML model"""
    load_model_artifacts()
