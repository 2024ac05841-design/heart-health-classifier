"""
Script to download the Heart Disease UCI Dataset
"""

import os
import pandas as pd
from pathlib import Path


def download_heart_disease_data():
    """
    Download Heart Disease UCI Dataset
    """
    print("Downloading Heart Disease UCI Dataset...")

    # Create data directories if they don't exist
    raw_data_dir = Path("data/raw")
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Try using ucimlrepo package first
        from ucimlrepo import fetch_ucirepo

        # Fetch dataset
        heart_disease = fetch_ucirepo(id=45)

        # Extract features and targets
        X = heart_disease.data.features
        y = heart_disease.data.targets

        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        print(f"Target column(s): {y.columns.tolist()}")
        
        # Combine into single dataframe
        df = pd.concat([X, y], axis=1)
        
        print(f"Combined dataframe columns: {df.columns.tolist()}")
        
        # Ensure target column is named 'target'
        # The UCI dataset may use 'num' or other names for the target
        if 'target' not in df.columns:
            # If there's a target column from y dataframe, rename it
            if len(y.columns) > 0:
                target_col = y.columns[0]
                print(f"Renaming '{target_col}' to 'target'")
                df = df.rename(columns={target_col: 'target'})
            else:
                raise ValueError(f"No target column found. Available columns: {df.columns.tolist()}")

        # Save to CSV
        output_path = raw_data_dir / "heart_disease.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Dataset downloaded successfully to {output_path}")
        print(f"✓ Dataset shape: {df.shape}")
        print(f"✓ Columns: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"Error with ucimlrepo: {e}")
        print("Attempting alternative download method...")

        # Alternative: Download from UCI repository directly
        import requests

        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

        # Column names for the dataset
        column_names = [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
            "target",
        ]

        try:
            response = requests.get(url)
            response.raise_for_status()

            # Save raw data
            with open(raw_data_dir / "heart.data", "w") as f:
                f.write(response.text)

            # Parse into DataFrame
            from io import StringIO

            df = pd.read_csv(StringIO(response.text), names=column_names, na_values="?")

            # Save to CSV
            output_path = raw_data_dir / "heart_disease.csv"
            df.to_csv(output_path, index=False)
            print(f"✓ Dataset downloaded successfully to {output_path}")
            print(f"✓ Dataset shape: {df.shape}")

            return df

        except Exception as e2:
            print(f"Error downloading data: {e2}")
            print("Please manually download the dataset from:")
            print("https://archive.ics.uci.edu/ml/datasets/Heart+Disease")
            return None


if __name__ == "__main__":
    df = download_heart_disease_data()
    if df is not None:
        print("\n" + "=" * 60)
        print("Dataset Preview:")
        print("=" * 60)
        print(df.head())
        print("\n" + "=" * 60)
        print("Dataset Info:")
        print("=" * 60)
        print(df.info())
