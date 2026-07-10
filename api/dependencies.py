"""
Dependency injection for model loading and shared state
"""

import joblib
import logging
from api.monitoring import active_model_info, model_loaded_status

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

        # Set Prometheus metrics for model monitoring
        model_type = type(model).__name__
        model_version = "1.0.0"  # Can be read from metadata file if available
        active_model_info.labels(model_type=model_type, version=model_version).set(1)
        model_loaded_status.set(1)

        logger.info("=" * 80)
        logger.info("🫀 Heart Disease Prediction API is ready!")
        logger.info("=" * 80)
        logger.info("📚 Interactive API Documentation (Swagger UI):")
        logger.info("   • http://localhost:30080/docs")
        logger.info("")
        logger.info("📊 Metrics & Monitoring:")
        logger.info("   • Prometheus Metrics:   http://localhost:30080/metrics")
        logger.info(
            "   • Prometheus Dashboard: http://localhost:30090 (deploy k8s/monitoring-local.yaml)"
        )
        logger.info(
            "   • Grafana Dashboard:    http://localhost:30030 (deploy k8s/monitoring-local.yaml)"
        )
        logger.info("     Default credentials: admin/admin")
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

        logger.info("")
        logger.info("📊 Monitoring & Visualization:")
        logger.info("   • Prometheus Metrics:  http://localhost:30080/metrics")
        logger.info("   • Grafana Dashboard:   http://localhost:3000")
        logger.info("     (Default credentials: admin/admin)")
        logger.info("=" * 80)
    except Exception as e:
        logger.error(f"✗ Error loading model: {e}")
        logger.warning("Model not loaded - predictions will fail")
        model_loaded_status.set(0)
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
