"""
Unit tests for model training module
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
from src.model_training import ModelTrainer, train_and_evaluate_models


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


def test_tune_hyperparameters_logistic(sample_classification_data):
    """Test hyperparameter tuning for Logistic Regression"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    param_grid = {"C": [0.1, 1.0], "penalty": ["l2"]}

    best_model, best_params = trainer.tune_hyperparameters(
        "logistic_regression", X, y, param_grid, cv=3
    )

    assert best_model is not None
    assert "C" in best_params
    assert hasattr(best_model, "predict")


def test_tune_hyperparameters_random_forest(sample_classification_data):
    """Test hyperparameter tuning for Random Forest"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    param_grid = {"n_estimators": [10, 20], "max_depth": [3, 5]}

    best_model, best_params = trainer.tune_hyperparameters(
        "random_forest", X, y, param_grid, cv=3
    )

    assert best_model is not None
    assert "n_estimators" in best_params
    assert "max_depth" in best_params


def test_tune_hyperparameters_invalid_model():
    """Test hyperparameter tuning with invalid model type"""
    X, y = make_classification(n_samples=50, n_features=5, random_state=42)

    trainer = ModelTrainer()
    param_grid = {"C": [0.1, 1.0]}

    with pytest.raises(ValueError, match="Unknown model type"):
        trainer.tune_hyperparameters("invalid_model", X, y, param_grid)


def test_plot_confusion_matrix(sample_classification_data, tmp_path):
    """Test confusion matrix plotting"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)
    y_pred = model.predict(X)

    # Save to temporary file
    save_path = tmp_path / "confusion_matrix.png"
    cm = trainer.plot_confusion_matrix(y, y_pred, str(save_path))

    assert cm is not None
    assert cm.shape == (2, 2)  # Binary classification
    assert save_path.exists()


def test_plot_confusion_matrix_without_save(sample_classification_data):
    """Test confusion matrix plotting without saving"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)
    y_pred = model.predict(X)

    cm = trainer.plot_confusion_matrix(y, y_pred)

    assert cm is not None
    assert cm.shape == (2, 2)


def test_plot_roc_curve(sample_classification_data, tmp_path):
    """Test ROC curve plotting"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)
    y_pred_proba = model.predict_proba(X)[:, 1]

    # Save to temporary file
    save_path = tmp_path / "roc_curve.png"
    fpr, tpr, roc_auc = trainer.plot_roc_curve(y, y_pred_proba, str(save_path))

    assert fpr is not None
    assert tpr is not None
    assert 0 <= roc_auc <= 1
    assert save_path.exists()


def test_plot_roc_curve_without_save(sample_classification_data):
    """Test ROC curve plotting without saving"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)
    y_pred_proba = model.predict_proba(X)[:, 1]

    fpr, tpr, roc_auc = trainer.plot_roc_curve(y, y_pred_proba)

    assert len(fpr) > 0
    assert len(tpr) > 0
    assert 0 <= roc_auc <= 1


def test_get_feature_importance_random_forest(sample_classification_data):
    """Test feature importance extraction from Random Forest"""
    X, y = sample_classification_data
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)

    importance_df = trainer.get_feature_importance(model, feature_names, top_n=5)

    assert importance_df is not None
    assert len(importance_df) == 5
    assert "feature" in importance_df.columns
    assert "importance" in importance_df.columns


def test_get_feature_importance_logistic_regression(sample_classification_data):
    """Test feature importance with model that doesn't support it"""
    X, y = sample_classification_data
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    importance_df = trainer.get_feature_importance(model, feature_names)

    # Logistic Regression doesn't have feature_importances_
    assert importance_df is None


def test_log_to_mlflow(sample_classification_data, tmp_path):
    """Test logging to MLflow"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    params = {"C": 1.0, "max_iter": 1000}
    metrics = {"accuracy": 0.85, "precision": 0.87}

    # Log to MLflow (will create a run)
    trainer.log_to_mlflow(model, "test_model", params, metrics)

    # Just verify it doesn't raise an exception
    assert True


def test_log_to_mlflow_with_artifacts(sample_classification_data, tmp_path):
    """Test logging to MLflow with artifacts"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)

    # Create dummy artifact
    artifact_path = tmp_path / "test_artifact.txt"
    artifact_path.write_text("Test artifact content")

    params = {"n_estimators": 10}
    metrics = {"accuracy": 0.90}
    artifacts = {"test_artifact": str(artifact_path)}

    trainer.log_to_mlflow(
        model, "test_model_with_artifacts", params, metrics, artifacts
    )

    # Just verify it doesn't raise an exception
    assert True


def test_train_and_evaluate_models(sample_classification_data):
    """Test training and evaluating multiple models"""
    from src.model_training import train_and_evaluate_models

    X, y = sample_classification_data

    # Split data
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

    assert "logistic_regression" in results
    assert "random_forest" in results

    # Check structure
    for model_name in ["logistic_regression", "random_forest"]:
        assert "model" in results[model_name]
        assert "metrics" in results[model_name]

        metrics = results[model_name]["metrics"]
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert "roc_auc" in metrics


def test_train_and_evaluate_models_with_feature_names(sample_classification_data):
    """Test train_and_evaluate_models with feature names"""
    from src.model_training import train_and_evaluate_models

    X, y = sample_classification_data
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    # Split data
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    results = train_and_evaluate_models(
        X_train, X_test, y_train, y_test, feature_names=feature_names
    )

    assert results is not None
    assert len(results) == 2


def test_trainer_custom_parameters(sample_classification_data):
    """Test training with custom parameters"""
    X, y = sample_classification_data

    trainer = ModelTrainer()

    # Train with custom parameters
    lr_model = trainer.train_logistic_regression(X, y, C=0.5, max_iter=500)
    assert lr_model.C == 0.5
    assert lr_model.max_iter == 500

    rf_model = trainer.train_random_forest(X, y, n_estimators=50, max_depth=5)
    assert rf_model.n_estimators == 50
    assert rf_model.max_depth == 5


def test_evaluate_model_without_name(sample_classification_data):
    """Test model evaluation without storing results"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_logistic_regression(X, y)

    metrics = trainer.evaluate_model(model, X, y)

    assert metrics is not None
    assert len(trainer.results) == 0  # Should not store results


def test_cross_validate_different_cv_folds(sample_classification_data):
    """Test cross-validation with different number of folds"""
    X, y = sample_classification_data

    trainer = ModelTrainer()
    model = trainer.train_random_forest(X, y, n_estimators=10)

    cv_results = trainer.cross_validate_model(model, X, y, cv=10)

    assert "f1_mean" in cv_results
    assert "roc_auc_mean" in cv_results
    assert cv_results["f1_mean"] >= 0
    assert cv_results["roc_auc_mean"] >= 0
