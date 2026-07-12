"""
Unit tests for feature engineering functions
"""

import pytest
import pandas as pd
import numpy as np
from src.feature_engineering import FeatureEngineer, build_preprocessing_pipeline


class TestFeatureEngineer:
    """Test suite for FeatureEngineer class"""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing"""
        return pd.DataFrame(
            {
                "age": [45, 55, 65, 75],
                "chol": [200, 250, 300, 350],
                "trestbps": [120, 140, 160, 180],
                "thalach": [150, 140, 130, 120],
                "fbs": [0, 1, 1, 1],
                "sex": [1, 0, 1, 0],
                "target": [0, 1, 1, 1],
            }
        )

    @pytest.fixture
    def feature_engineer(self):
        """Create FeatureEngineer instance"""
        return FeatureEngineer()

    def test_feature_engineer_initialization(self, feature_engineer):
        """Test FeatureEngineer initialization"""
        assert feature_engineer.feature_names is None
        assert feature_engineer.transformer is None

    def test_create_age_groups(self, feature_engineer, sample_df):
        """Test age group creation"""
        result = feature_engineer.create_age_groups(sample_df)

        assert "age_group" in result.columns
        assert len(result) == len(sample_df)
        # Bins: [0, 40, 50, 60, 100] -> labels: ['young', 'middle', 'senior', 'elderly']
        assert result["age_group"].iloc[0] == "middle"  # age 45 (40-50)
        assert result["age_group"].iloc[1] == "senior"  # age 55 (50-60)
        assert result["age_group"].iloc[2] == "elderly"  # age 65 (60-100)
        assert result["age_group"].iloc[3] == "elderly"  # age 75 (60-100)

    def test_create_age_groups_preserves_original(self, feature_engineer, sample_df):
        """Test that create_age_groups doesn't modify original DataFrame"""
        original_columns = sample_df.columns.tolist()
        result = feature_engineer.create_age_groups(sample_df)

        assert sample_df.columns.tolist() == original_columns
        assert "age_group" not in sample_df.columns

    def test_create_interaction_features(self, feature_engineer, sample_df):
        """Test interaction feature creation"""
        result = feature_engineer.create_interaction_features(sample_df)

        assert "age_chol_interaction" in result.columns
        assert "bp_hr_ratio" in result.columns

        # Verify calculations
        expected_age_chol = sample_df["age"] * sample_df["chol"]
        pd.testing.assert_series_equal(
            result["age_chol_interaction"], expected_age_chol, check_names=False
        )

        expected_ratio = sample_df["trestbps"] / (sample_df["thalach"] + 1)
        pd.testing.assert_series_equal(
            result["bp_hr_ratio"], expected_ratio, check_names=False
        )

    def test_create_interaction_features_missing_columns(self, feature_engineer):
        """Test interaction features with missing columns"""
        df = pd.DataFrame({"other_col": [1, 2, 3]})
        result = feature_engineer.create_interaction_features(df)

        assert "age_chol_interaction" not in result.columns
        assert "bp_hr_ratio" not in result.columns

    def test_create_risk_score(self, feature_engineer, sample_df):
        """Test risk score calculation"""
        result = feature_engineer.create_risk_score(sample_df)

        assert "risk_score" in result.columns

        # Age 45, chol 200, trestbps 120, fbs 0 -> risk_score = 0
        assert result["risk_score"].iloc[0] == 0

        # Age 65, chol 300, trestbps 160, fbs 1 -> risk_score = 4 (age>60, chol>240, trestbps>140, fbs=1)
        assert result["risk_score"].iloc[2] == 4

        # Age 75, chol 350, trestbps 180, fbs 1 -> risk_score = 4
        assert result["risk_score"].iloc[3] == 4

    def test_create_risk_score_empty_df(self, feature_engineer):
        """Test risk score with empty DataFrame"""
        df = pd.DataFrame({"other_col": [1, 2, 3]})
        result = feature_engineer.create_risk_score(df)

        assert "risk_score" not in result.columns

    def test_select_features(self, feature_engineer, sample_df):
        """Test feature selection"""
        feature_list = ["age", "chol", "trestbps"]
        result = feature_engineer.select_features(sample_df, feature_list)

        assert result.columns.tolist() == feature_list
        assert len(result) == len(sample_df)

    def test_select_features_partial_match(self, feature_engineer, sample_df):
        """Test feature selection with some non-existent features"""
        feature_list = ["age", "chol", "nonexistent_feature"]
        result = feature_engineer.select_features(sample_df, feature_list)

        assert "age" in result.columns
        assert "chol" in result.columns
        assert "nonexistent_feature" not in result.columns

    def test_select_features_none(self, feature_engineer, sample_df):
        """Test feature selection with None"""
        result = feature_engineer.select_features(sample_df, None)

        pd.testing.assert_frame_equal(result, sample_df)

    def test_get_feature_names(self, feature_engineer, sample_df):
        """Test getting feature names"""
        feature_names = feature_engineer.get_feature_names(sample_df)

        assert isinstance(feature_names, list)
        assert feature_names == sample_df.columns.tolist()


class TestBuildPreprocessingPipeline:
    """Test suite for build_preprocessing_pipeline function"""

    def test_build_pipeline_numerical_only(self):
        """Test pipeline with only numerical features"""
        numerical_features = ["age", "chol", "trestbps"]
        pipeline = build_preprocessing_pipeline(numerical_features)

        assert pipeline is not None
        assert "preprocessor" in pipeline.named_steps

    def test_build_pipeline_with_categorical(self):
        """Test pipeline with numerical and categorical features"""
        numerical_features = ["age", "chol", "trestbps"]
        categorical_features = ["sex", "cp"]
        pipeline = build_preprocessing_pipeline(
            numerical_features, categorical_features
        )

        assert pipeline is not None
        assert "preprocessor" in pipeline.named_steps

        # Check that both transformers are present
        preprocessor = pipeline.named_steps["preprocessor"]
        assert len(preprocessor.transformers) == 2

    def test_build_pipeline_fit_transform(self):
        """Test that pipeline can fit and transform data"""
        df = pd.DataFrame(
            {"age": [45, 55, 65], "chol": [200, 250, 300], "sex": ["M", "F", "M"]}
        )

        numerical_features = ["age", "chol"]
        categorical_features = ["sex"]
        pipeline = build_preprocessing_pipeline(
            numerical_features, categorical_features
        )

        # Should not raise any errors
        transformed = pipeline.fit_transform(df)

        assert transformed is not None
        assert transformed.shape[0] == 3
