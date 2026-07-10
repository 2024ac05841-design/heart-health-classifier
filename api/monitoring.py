"""
Prometheus metrics for ML model monitoring

Custom metrics to track model predictions, confidence scores,
inference performance, and model versioning.
"""

from prometheus_client import Counter, Histogram, Gauge

# Prediction metrics
predictions_counter = Counter(
    "heart_disease_predictions_total",
    "Total heart disease predictions made",
    ["prediction_class", "risk_level"],
)

prediction_confidence_hist = Histogram(
    "heart_disease_prediction_confidence",
    "Distribution of prediction confidence scores",
    buckets=[0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99, 1.0],
)

prediction_risk_score_hist = Histogram(
    "heart_disease_risk_score",
    "Distribution of risk scores (probability of disease)",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

model_inference_time = Histogram(
    "model_inference_seconds",
    "Time taken for model inference only (excluding preprocessing)",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

preprocessing_time = Histogram(
    "data_preprocessing_seconds",
    "Time taken for data preprocessing (scaling, transformation)",
    buckets=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1],
)

active_model_info = Gauge(
    "active_model_info",
    "Information about the currently loaded model",
    ["model_type", "version"],
)

model_loaded_status = Gauge(
    "model_loaded_status",
    "Whether the ML model is successfully loaded (1=loaded, 0=not loaded)",
)

# Feature statistics (for data drift detection)
feature_value_hist = Histogram(
    "input_feature_value",
    "Distribution of input feature values",
    ["feature_name"],
    buckets=[0, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500],
)
