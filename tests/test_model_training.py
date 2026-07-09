"""
Unit tests for model training module
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from src.model_training import ModelTrainer


@pytest.fixture
def sample_classification_data():
    """Create sample classification data"""
    X, y = make_classification(
        n_samples=100, n_features=10, n_informative=5, n_redundant=2, random_state=42
    )
    return pd.DataFrame(X), pd.Series(y)


def test_model_trainer_init():
    """Test ModelTrainer initialization"""
    trainer = ModelTrainer(experiment_name="test_experiment")
    assert trainer.experiment_name == "test_experiment"
    assert len(trainer.models) == 0
    assert len(trainer.results) == 0


def test_train_logistic_regression(sample_classification_data):
    """Test Logistic Regression training"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    assert model is not None
    assert hasattr(model, "predict")
    assert "logistic_regression" in trainer.models


def test_train_random_forest(sample_classification_data):
    """Test Random Forest training"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)

    assert model is not None
    assert hasattr(model, "predict")
    assert "random_forest" in trainer.models


def test_evaluate_model(sample_classification_data):
    """Test model evaluation"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    metrics = trainer.evaluate_model(model, X, y, model_name="test_model")

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics

    # Check metric ranges
    for metric_name, metric_value in metrics.items():
        assert 0 <= metric_value <= 1


def test_cross_validate_model(sample_classification_data):
    """Test cross-validation"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    cv_results = trainer.cross_validate_model(model, X, y, cv=3)

    assert "accuracy_mean" in cv_results
    assert "accuracy_std" in cv_results
    assert 0 <= cv_results["accuracy_mean"] <= 1


def test_model_predictions(sample_classification_data):
    """Test model predictions"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    assert len(predictions) == len(X)
    assert probabilities.shape[0] == len(X)
    assert probabilities.shape[1] == 2  # Binary classification

    # Check probabilities sum to 1
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_save_load_model(sample_classification_data, tmp_path):
    """Test model saving and loading"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    # Save model
    model_path = tmp_path / "test_model.pkl"
    trainer.save_model(model, str(model_path))

    assert model_path.exists()

    # Load model
    loaded_model = trainer.load_model(str(model_path))

    # Test loaded model
    predictions_original = model.predict(X)
    predictions_loaded = loaded_model.predict(X)

    assert np.array_equal(predictions_original, predictions_loaded)
