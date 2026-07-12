"""
Register the best model to MLflow Model Registry
"""

import mlflow
from mlflow.tracking import MlflowClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_best_model():
    """Register the best performing model to MLflow Model Registry"""

    # Set MLflow tracking URI to local Kubernetes service
    mlflow.set_tracking_uri("http://localhost:30050")

    # Initialize MLflow client
    client = MlflowClient()

    # Best model details (Random Forest - 98.4% accuracy)
    run_id = "877944cc37004c99a8d0c3aa31e693e9"
    model_name = "heart-disease-predictor"
    model_artifact_path = "random_forest"

    logger.info("=" * 60)
    logger.info("Registering Best Model to MLflow Model Registry")
    logger.info("=" * 60)

    try:
        # Create model URI
        model_uri = f"runs:/{run_id}/{model_artifact_path}"
        logger.info(f"\nModel URI: {model_uri}")

        # Register the model
        logger.info(f"\nRegistering model as '{model_name}'...")
        model_version = mlflow.register_model(
            model_uri=model_uri,
            name=model_name,
            tags={
                "model_type": "RandomForest",
                "accuracy": "0.984",
                "roc_auc": "1.0",
                "trained_on": "2026-07-12",
                "description": "Best performing heart disease prediction model",
            },
        )

        logger.info(f"✓ Model registered successfully!")
        logger.info(f"  Name: {model_version.name}")
        logger.info(f"  Version: {model_version.version}")
        logger.info(f"  Run ID: {model_version.run_id}")

        # Add model version description
        logger.info(f"\nAdding model description...")
        client.update_model_version(
            name=model_name,
            version=model_version.version,
            description=(
                "Random Forest classifier trained on heart disease dataset. "
                "Achieves 98.4% accuracy with 100% recall on test set. "
                "Uses 100 estimators with balanced class weights."
            ),
        )

        # Add registered model description
        logger.info(f"Adding registered model description...")
        client.update_registered_model(
            name=model_name,
            description=(
                "Heart Disease Prediction Model for production deployment. "
                "Predicts presence of heart disease based on patient health metrics."
            ),
        )

        # Transition to Production stage
        logger.info(f"\nTransitioning model to Production stage...")
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Production",
            archive_existing_versions=False,
        )

        logger.info(f"✓ Model transitioned to Production!")

        logger.info("\n" + "=" * 60)
        logger.info("MODEL REGISTRATION COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"\nYou can now load the model using:")
        logger.info(
            f"  model = mlflow.pyfunc.load_model('models:/{model_name}/Production')"
        )
        logger.info(f"\nView in UI: http://localhost:30050/#/models/{model_name}")

        return model_version

    except Exception as e:
        logger.error(f"Error registering model: {e}")
        raise


if __name__ == "__main__":
    register_best_model()
