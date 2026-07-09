"""
Data processing and preprocessing functions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle all data processing operations"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.numerical_features = None
        self.categorical_features = None

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Data loaded successfully: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        logger.info(f"Missing values before processing:\n{df.isnull().sum()}")

        # For numerical columns: fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())

        # For categorical columns: fill with mode
        categorical_cols = df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mode()[0])

        logger.info(f"Missing values after processing:\n{df.isnull().sum()}")
        return df

    def encode_target(
        self, df: pd.DataFrame, target_col: str = "target"
    ) -> pd.DataFrame:
        """Encode target variable as binary (0: no disease, 1: disease)"""
        if target_col in df.columns:
            # Convert multi-class target to binary
            df[target_col] = (df[target_col] > 0).astype(int)
            logger.info(f"Target distribution:\n{df[target_col].value_counts()}")
        return df

    def split_features_target(
        self, df: pd.DataFrame, target_col: str = "target"
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Split features and target"""
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataframe")

        X = df.drop(columns=[target_col])
        y = df[target_col]

        logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
        return X, y

    def split_train_test(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> Tuple:
        """Split data into train and test sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
        logger.info(f"Train target distribution:\n{y_train.value_counts()}")
        logger.info(f"Test target distribution:\n{y_test.value_counts()}")

        return X_train, X_test, y_train, y_test

    def scale_features(
        self, X_train: pd.DataFrame, X_test: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Scale numerical features"""
        # Fit scaler on training data
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index,
        )

        # Transform test data
        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test), columns=X_test.columns, index=X_test.index
        )

        logger.info("Features scaled successfully")
        return X_train_scaled, X_test_scaled

    def preprocess_pipeline(
        self, filepath: str, target_col: str = "target", test_size: float = 0.2
    ) -> Tuple:
        """Complete preprocessing pipeline"""
        # Load data
        df = self.load_data(filepath)

        # Handle missing values
        df = self.handle_missing_values(df)

        # Encode target
        df = self.encode_target(df, target_col)

        # Split features and target
        X, y = self.split_features_target(df, target_col)

        # Split train/test
        X_train, X_test, y_train, y_test = self.split_train_test(X, y, test_size)

        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)

        logger.info("Preprocessing pipeline completed successfully")
        return X_train_scaled, X_test_scaled, y_train, y_test


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Utility function to load and clean data"""
    processor = DataProcessor()
    df = processor.load_data(filepath)
    df = processor.handle_missing_values(df)
    df = processor.encode_target(df)
    return df
