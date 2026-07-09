"""
Feature engineering functions
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Feature engineering operations"""

    def __init__(self):
        self.feature_names = None
        self.transformer = None

    def create_age_groups(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create age group categories"""
        df = df.copy()
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 40, 50, 60, 100],
            labels=["young", "middle", "senior", "elderly"],
        )
        return df

    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features"""
        df = df.copy()

        # Age and cholesterol interaction
        if "age" in df.columns and "chol" in df.columns:
            df["age_chol_interaction"] = df["age"] * df["chol"]

        # Blood pressure and heart rate interaction
        if "trestbps" in df.columns and "thalach" in df.columns:
            df["bp_hr_ratio"] = df["trestbps"] / (df["thalach"] + 1)

        return df

    def create_risk_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create composite risk score"""
        df = df.copy()

        risk_factors = []

        if "age" in df.columns:
            risk_factors.append((df["age"] > 60).astype(int))

        if "chol" in df.columns:
            risk_factors.append((df["chol"] > 240).astype(int))

        if "trestbps" in df.columns:
            risk_factors.append((df["trestbps"] > 140).astype(int))

        if "fbs" in df.columns:
            risk_factors.append(df["fbs"].astype(int))

        if risk_factors:
            df["risk_score"] = sum(risk_factors)

        return df

    def select_features(
        self, df: pd.DataFrame, feature_list: list = None
    ) -> pd.DataFrame:
        """Select specific features"""
        if feature_list:
            available_features = [f for f in feature_list if f in df.columns]
            df = df[available_features]
            logger.info(f"Selected {len(available_features)} features")
        return df

    def get_feature_names(self, df: pd.DataFrame) -> list:
        """Get list of feature names"""
        return list(df.columns)


def build_preprocessing_pipeline(
    numerical_features: list, categorical_features: list = None
) -> Pipeline:
    """
    Build a complete preprocessing pipeline

    Args:
        numerical_features: List of numerical feature names
        categorical_features: List of categorical feature names (optional)

    Returns:
        sklearn Pipeline object
    """
    from sklearn.preprocessing import StandardScaler, OneHotEncoder

    transformers = [("num", StandardScaler(), numerical_features)]

    if categorical_features:
        transformers.append(
            (
                "cat",
                OneHotEncoder(drop="first", sparse_output=False),
                categorical_features,
            )
        )

    preprocessor = ColumnTransformer(transformers=transformers, remainder="passthrough")

    pipeline = Pipeline([("preprocessor", preprocessor)])

    logger.info("Preprocessing pipeline created")
    return pipeline
