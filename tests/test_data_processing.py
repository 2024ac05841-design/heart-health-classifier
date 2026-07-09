"""
Unit tests for data processing module
"""

import pytest
import pandas as pd
import numpy as np
from src.data_processing import DataProcessor


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame(
        {
            "age": [63, 67, 67, 37, 41, 56, 62, 57, 63, 53, 57, 56, 44, 52, 57, 54, 48, 49, 64, 58],
            "sex": [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            "cp": [3, 0, 0, 2, 1, 1, 0, 1, 3, 2, 0, 1, 1, 2, 2, 1, 1, 1, 3, 3],
            "trestbps": [145, 160, 120, 130, 130, 120, 140, 120, 130, 140, 140, 140, 120, 172, 132, 108, 130, 130, 120, 150],
            "chol": [233, 286, 229, 250, 204, 236, 268, 354, 254, 203, 192, 294, 263, 199, 168, 267, 275, 266, 177, 270],
            "fbs": [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            "restecg": [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1],
            "thalach": [150, 108, 129, 187, 172, 178, 160, 163, 147, 155, 148, 153, 173, 162, 174, 167, 139, 171, 106, 132],
            "exang": [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
            "oldpeak": [2.3, 1.5, 2.6, 3.5, 1.4, 0.8, 3.6, 0.6, 1.4, 3.1, 0.4, 1.3, 0.0, 0.5, 1.6, 0.0, 0.2, 0.6, 2.2, 1.2],
            "slope": [0, 1, 1, 0, 2, 2, 0, 2, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1],
            "ca": [0, 3, 2, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
            "thal": [1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 3, 3, 2, 2, 2, 2, 3, 2],
            "target": [1, 2, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
        }
    )


def test_data_processor_init():
    """Test DataProcessor initialization"""
    processor = DataProcessor()
    assert processor.scaler is not None
    assert processor.numerical_features is None
    assert processor.categorical_features is None


def test_load_data(sample_data, tmp_path):
    """Test data loading"""
    # Save sample data to temp file
    temp_file = tmp_path / "test_data.csv"
    sample_data.to_csv(temp_file, index=False)

    # Load data
    processor = DataProcessor()
    df = processor.load_data(str(temp_file))

    assert df.shape == sample_data.shape
    assert list(df.columns) == list(sample_data.columns)


def test_handle_missing_values():
    """Test missing value handling"""
    # Create data with missing values
    df = pd.DataFrame(
        {
            "age": [63, np.nan, 67, 37, 41],
            "sex": [1, 1, np.nan, 1, 0],
            "target": [1, 0, 1, 0, 0],
        }
    )

    processor = DataProcessor()
    df_clean = processor.handle_missing_values(df)

    assert df_clean.isnull().sum().sum() == 0


def test_encode_target(sample_data):
    """Test target encoding"""
    processor = DataProcessor()
    df_encoded = processor.encode_target(sample_data.copy())

    # Target should be binary
    assert df_encoded["target"].nunique() <= 2
    assert set(df_encoded["target"].unique()).issubset({0, 1})


def test_split_features_target(sample_data):
    """Test feature-target split"""
    processor = DataProcessor()
    X, y = processor.split_features_target(sample_data)

    assert "target" not in X.columns
    assert len(X) == len(y)
    assert len(X.columns) == len(sample_data.columns) - 1


def test_split_train_test(sample_data):
    """Test train-test split"""
    processor = DataProcessor()
    X, y = processor.split_features_target(sample_data)

    X_train, X_test, y_train, y_test = processor.split_train_test(
        X, y, test_size=0.2, random_state=42
    )

    assert len(X_train) + len(X_test) == len(X)
    assert len(y_train) + len(y_test) == len(y)
    assert len(X_train) > len(X_test)


def test_scale_features(sample_data):
    """Test feature scaling"""
    processor = DataProcessor()
    X, y = processor.split_features_target(sample_data)
    X_train, X_test, y_train, y_test = processor.split_train_test(X, y, test_size=0.2)

    X_train_scaled, X_test_scaled = processor.scale_features(X_train, X_test)

    assert X_train_scaled.shape == X_train.shape
    assert X_test_scaled.shape == X_test.shape

    # Check that scaling was applied (mean should be close to 0)
    assert abs(X_train_scaled.mean().mean()) < 1


def test_preprocess_pipeline(sample_data, tmp_path):
    """Test complete preprocessing pipeline"""
    # Save sample data
    temp_file = tmp_path / "test_data.csv"
    sample_data.to_csv(temp_file, index=False)

    processor = DataProcessor()
    X_train, X_test, y_train, y_test = processor.preprocess_pipeline(str(temp_file))

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)
