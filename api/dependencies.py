"""
Dependency injection for model loading and shared state
"""

import joblib
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Global state for model and artifacts
model = None
scaler = None
feature_names = None


def load_model_artifacts():
    """Load model and preprocessing artifacts at startup"""
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

        logger.info("✓ Model and artifacts loaded successfully")
        logger.info("=" * 80)
        logger.info("🫀 Heart Disease Prediction API is ready!")
        logger.info("=" * 80)
        logger.info("📚 Interactive API Documentation (Swagger UI):")
        logger.info("   • Container: http://localhost:8000/docs")
        logger.info("   • Kubernetes: http://localhost:30080/docs")
        logger.info("")
        logger.info("🧪 Testing the API:")
        logger.info("   1. Visit the Swagger UI at /docs")
        logger.info(
            "   2. Try the /generate-test-data endpoint to create sample patient data"
        )
        logger.info("   3. Copy the generated data and use it in the /predict endpoint")
        logger.info("")
        logger.info("🔍 Available Endpoints:")
        logger.info("   • POST /predict             - Heart disease prediction")
        logger.info("   • GET  /model/info          - Model information")
        logger.info("   • GET  /generate-test-data  - Generate sample test data")
        logger.info("   • GET  /metrics             - Prometheus metrics")
        logger.info("")
        logger.info("💡 Access via:")
        logger.info("   - Direct Docker: http://localhost:8000")
        logger.info("   - Kubernetes (NodePort): http://localhost:30080")
        logger.info("=" * 80)
    except Exception as e:
        logger.error(f"✗ Error loading model: {e}")
        logger.warning("Model not loaded - predictions will fail")
        logger.info("=" * 80)


def get_model():
    """Dependency to get the loaded model"""
    return model


def get_scaler():
    """Dependency to get the loaded scaler"""
    return scaler


def get_feature_names():
    """Dependency to get feature names"""
    return feature_names
