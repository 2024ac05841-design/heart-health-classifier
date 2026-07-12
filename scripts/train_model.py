"""
Main training script
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_processing import DataProcessor
from src.model_training import ModelTrainer
from src.utils import ensure_dir, save_model_artifacts
import mlflow
import joblib

# Configure MLflow tracking directory
mlflow.set_tracking_uri("file:./mlruns_training")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Train heart disease prediction models"
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="data/raw/heart_disease.csv",
        help="Path to the dataset",
    )
    parser.add_argument(
        "--output-dir", type=str, default="models", help="Output directory for models"
    )
    parser.add_argument(
        "--experiment-name",
        type=str,
        default="heart_disease_prediction",
        help="MLflow experiment name",
    )
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set size")
    return parser.parse_args()


def main():
    """Main training function"""
    args = parse_args()

    logger.info("=" * 60)
    logger.info("Starting Heart Disease Prediction Model Training")
    logger.info("=" * 60)

    # Ensure output directory exists
    ensure_dir(args.output_dir)

    # Step 1: Load and preprocess data
    logger.info("\n[Step 1/4] Loading and preprocessing data...")
    processor = DataProcessor()
    X_train, X_test, y_train, y_test = processor.preprocess_pipeline(
        args.data_path, test_size=args.test_size
    )

    # Get feature names
    feature_names = list(X_train.columns)
    logger.info(f"Features: {feature_names}")

    # Step 2: Initialize trainer
    logger.info("\n[Step 2/4] Initializing model trainer...")
    trainer = ModelTrainer(experiment_name=args.experiment_name)

    # Step 3: Train models
    logger.info("\n[Step 3/4] Training models...")

    # Train Logistic Regression
    logger.info("\nTraining Logistic Regression...")
    lr_model = trainer.train_logistic_regression(X_train, y_train)
    lr_metrics = trainer.evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    lr_cv_results = trainer.cross_validate_model(lr_model, X_train, y_train)

    # Log to MLflow
    lr_params = {
        "model_type": "LogisticRegression",
        "test_size": args.test_size,
        "random_state": 42,
    }
    trainer.log_to_mlflow(lr_model, "logistic_regression", lr_params, lr_metrics)

    # Train Random Forest
    logger.info("\nTraining Random Forest...")
    rf_model = trainer.train_random_forest(X_train, y_train, n_estimators=100)
    rf_metrics = trainer.evaluate_model(rf_model, X_test, y_test, "Random Forest")
    rf_cv_results = trainer.cross_validate_model(rf_model, X_train, y_train)

    # Log to MLflow
    rf_params = {
        "model_type": "RandomForest",
        "n_estimators": 100,
        "test_size": args.test_size,
        "random_state": 42,
    }
    trainer.log_to_mlflow(rf_model, "random_forest", rf_params, rf_metrics)

    # Step 4: Save ALL models (individual + best)
    logger.info("\n[Step 4/4] Saving models...")

    # Save individual models
    logger.info("\nSaving individual models...")
    joblib.dump(lr_model, os.path.join(args.output_dir, "logistic_regression.pkl"))
    logger.info(
        f"  - Logistic Regression saved: {args.output_dir}/logistic_regression.pkl"
    )

    joblib.dump(rf_model, os.path.join(args.output_dir, "random_forest.pkl"))
    logger.info(f"  - Random Forest saved: {args.output_dir}/random_forest.pkl")

    # Compare models by ROC-AUC and select best
    logger.info("\nSelecting best model...")
    if rf_metrics["roc_auc"] > lr_metrics["roc_auc"]:
        best_model = rf_model
        best_model_name = "Random Forest"
        best_metrics = rf_metrics
        best_model_type = "random_forest"
    else:
        best_model = lr_model
        best_model_name = "Logistic Regression"
        best_metrics = lr_metrics
        best_model_type = "logistic_regression"

    logger.info(f"\nBest Model: {best_model_name}")
    logger.info(f"ROC-AUC: {best_metrics['roc_auc']:.4f}")
    logger.info(f"Accuracy: {best_metrics['accuracy']:.4f}")

    # Save best model and artifacts
    joblib.dump(best_model, os.path.join(args.output_dir, "best_model.pkl"))
    joblib.dump(processor.scaler, os.path.join(args.output_dir, "scaler.pkl"))

    import json

    with open(os.path.join(args.output_dir, "feature_names.json"), "w") as f:
        json.dump({"features": feature_names}, f)

    with open(os.path.join(args.output_dir, "metrics.json"), "w") as f:
        json.dump(
            {
                "best_model": best_model_name,
                "best_model_type": best_model_type,
                "metrics": best_metrics,
                "logistic_regression_metrics": lr_metrics,
                "random_forest_metrics": rf_metrics,
            },
            f,
            indent=4,
        )

    logger.info(f"\nAll model artifacts saved to {args.output_dir}/:")
    logger.info(f"  - logistic_regression.pkl")
    logger.info(f"  - random_forest.pkl")
    logger.info(f"  - best_model.pkl ({best_model_name})")
    logger.info(f"  - scaler.pkl")
    logger.info(f"  - feature_names.json")
    logger.info(f"  - metrics.json (includes all metrics)")
    logger.info("\n" + "=" * 60)
    logger.info("Training completed successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
