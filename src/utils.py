"""
Utility functions
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_dir(directory: str):
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory ensured: {directory}")


def save_json(data: Dict, filepath: str):
    """Save dictionary to JSON file"""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON saved to {filepath}")


def load_json(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, "r") as f:
        data = json.load(f)
    logger.info(f"JSON loaded from {filepath}")
    return data


def save_model_artifacts(model, scaler, feature_names: list, output_dir: str):
    """Save model and related artifacts"""
    ensure_dir(output_dir)

    # Save model
    model_path = os.path.join(output_dir, "model.pkl")
    joblib.dump(model, model_path)

    # Save scaler
    scaler_path = os.path.join(output_dir, "scaler.pkl")
    joblib.dump(scaler, scaler_path)

    # Save feature names
    features_path = os.path.join(output_dir, "feature_names.json")
    save_json({"features": feature_names}, features_path)

    logger.info(f"Model artifacts saved to {output_dir}")


def load_model_artifacts(model_dir: str) -> Dict[str, Any]:
    """Load model and related artifacts"""
    artifacts = {}

    # Load model
    model_path = os.path.join(model_dir, "model.pkl")
    artifacts["model"] = joblib.load(model_path)

    # Load scaler
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    artifacts["scaler"] = joblib.load(scaler_path)

    # Load feature names
    features_path = os.path.join(model_dir, "feature_names.json")
    artifacts["feature_names"] = load_json(features_path)["features"]

    logger.info(f"Model artifacts loaded from {model_dir}")
    return artifacts


def setup_logging(log_file: str = "app.log"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
