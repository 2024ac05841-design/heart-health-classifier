"""
Model training and evaluation functions
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
)
import mlflow
import mlflow.sklearn
import joblib
import logging
from typing import Dict, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Handle model training and evaluation"""

    def __init__(self, experiment_name: str = "heart_disease_prediction"):
        self.experiment_name = experiment_name
        self.models = {}
        self.results = {}
        mlflow.set_experiment(experiment_name)

    def train_logistic_regression(
        self, X_train, y_train, **kwargs
    ) -> LogisticRegression:
        """Train Logistic Regression model"""
        logger.info("Training Logistic Regression...")

        model = LogisticRegression(
            random_state=kwargs.get("random_state", 42),
            max_iter=kwargs.get("max_iter", 1000),
            **{
                k: v for k, v in kwargs.items() if k not in ["random_state", "max_iter"]
            },
        )

        model.fit(X_train, y_train)
        self.models["logistic_regression"] = model
        logger.info("Logistic Regression trained successfully")

        return model

    def train_random_forest(self, X_train, y_train, **kwargs) -> RandomForestClassifier:
        """Train Random Forest model"""
        logger.info("Training Random Forest...")

        model = RandomForestClassifier(
            random_state=kwargs.get("random_state", 42),
            n_estimators=kwargs.get("n_estimators", 100),
            **{
                k: v
                for k, v in kwargs.items()
                if k not in ["random_state", "n_estimators"]
            },
        )

        model.fit(X_train, y_train)
        self.models["random_forest"] = model
        logger.info("Random Forest trained successfully")

        return model

    def evaluate_model(self, model, X_test, y_test, model_name: str = None) -> Dict:
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_pred_proba),
        }

        if model_name:
            self.results[model_name] = metrics
            logger.info(f"\n{model_name} Metrics:")
            for metric, value in metrics.items():
                logger.info(f"  {metric}: {value:.4f}")

        return metrics

    def cross_validate_model(self, model, X, y, cv: int = 5) -> Dict:
        """Perform cross-validation"""
        logger.info(f"Performing {cv}-fold cross-validation...")

        scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
        cv_results = {}

        for score in scoring:
            scores = cross_val_score(model, X, y, cv=cv, scoring=score)
            cv_results[f"{score}_mean"] = scores.mean()
            cv_results[f"{score}_std"] = scores.std()
            logger.info(f"  {score}: {scores.mean():.4f} (+/- {scores.std():.4f})")

        return cv_results

    def tune_hyperparameters(
        self, model_type: str, X_train, y_train, param_grid: Dict, cv: int = 5
    ) -> Tuple[Any, Dict]:
        """Tune hyperparameters using GridSearchCV"""
        logger.info(f"Tuning hyperparameters for {model_type}...")

        if model_type == "logistic_regression":
            base_model = LogisticRegression(random_state=42, max_iter=1000)
        elif model_type == "random_forest":
            base_model = RandomForestClassifier(random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        grid_search = GridSearchCV(
            base_model, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1, verbose=1
        )

        grid_search.fit(X_train, y_train)

        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best ROC-AUC score: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_, grid_search.best_params_

    def plot_confusion_matrix(self, y_test, y_pred, save_path: str = None):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["No Disease", "Disease"],
            yticklabels=["No Disease", "Disease"],
        )
        plt.title("Confusion Matrix")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Confusion matrix saved to {save_path}")

        return cm

    def plot_roc_curve(self, y_test, y_pred_proba, save_path: str = None):
        """Plot ROC curve"""
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        plt.figure(figsize=(8, 6))
        plt.plot(
            fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})"
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic (ROC) Curve")
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"ROC curve saved to {save_path}")

        return fpr, tpr, roc_auc

    def log_to_mlflow(
        self,
        model,
        model_name: str,
        params: Dict,
        metrics: Dict,
        artifacts: Dict = None,
    ):
        """Log model, parameters, and metrics to MLflow"""
        with mlflow.start_run(run_name=model_name):
            # Log parameters
            mlflow.log_params(params)

            # Log metrics
            mlflow.log_metrics(metrics)

            # Log model
            mlflow.sklearn.log_model(model, model_name)

            # Log artifacts
            if artifacts:
                for artifact_name, artifact_path in artifacts.items():
                    mlflow.log_artifact(artifact_path, artifact_name)

            logger.info(f"Model {model_name} logged to MLflow")

    def save_model(self, model, filepath: str):
        """Save model to disk"""
        joblib.dump(model, filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load model from disk"""
        model = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")
        return model

    def get_feature_importance(self, model, feature_names: list, top_n: int = 10):
        """Get feature importance for tree-based models"""
        if hasattr(model, "feature_importances_"):
            importance_df = pd.DataFrame(
                {"feature": feature_names, "importance": model.feature_importances_}
            ).sort_values("importance", ascending=False)

            return importance_df.head(top_n)
        else:
            logger.warning("Model does not have feature_importances_ attribute")
            return None


def train_and_evaluate_models(
    X_train, X_test, y_train, y_test, feature_names: list = None
) -> Dict:
    """
    Train and evaluate multiple models

    Returns:
        Dictionary containing trained models and their metrics
    """
    trainer = ModelTrainer()
    results = {}

    # Train Logistic Regression
    lr_model = trainer.train_logistic_regression(X_train, y_train)
    lr_metrics = trainer.evaluate_model(lr_model, X_test, y_test, "logistic_regression")
    results["logistic_regression"] = {"model": lr_model, "metrics": lr_metrics}

    # Train Random Forest
    rf_model = trainer.train_random_forest(X_train, y_train, n_estimators=100)
    rf_metrics = trainer.evaluate_model(rf_model, X_test, y_test, "random_forest")
    results["random_forest"] = {"model": rf_model, "metrics": rf_metrics}

    return results
