"""
Create sample heart disease dataset for testing
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Create data directory
data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data (303 samples as in original dataset)
n_samples = 303

data = {
    "age": np.random.randint(29, 78, n_samples),
    "sex": np.random.randint(0, 2, n_samples),
    "cp": np.random.randint(0, 4, n_samples),
    "trestbps": np.random.randint(94, 200, n_samples),
    "chol": np.random.randint(126, 565, n_samples),
    "fbs": np.random.randint(0, 2, n_samples),
    "restecg": np.random.randint(0, 3, n_samples),
    "thalach": np.random.randint(71, 202, n_samples),
    "exang": np.random.randint(0, 2, n_samples),
    "oldpeak": np.random.uniform(0, 6.2, n_samples).round(1),
    "slope": np.random.randint(0, 3, n_samples),
    "ca": np.random.randint(0, 4, n_samples),
    "thal": np.random.randint(0, 3, n_samples),
}

# Create target with realistic correlation to features
# Higher age, cp, and oldpeak increase disease probability
target_prob = (
    (data["age"] > 60).astype(int) * 0.3
    + (data["cp"] >= 2).astype(int) * 0.25
    + (data["oldpeak"] > 2).astype(int) * 0.25
    + np.random.uniform(0, 0.2, n_samples)
)

data["target"] = (target_prob > 0.5).astype(int)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_path = data_dir / "heart_disease.csv"
df.to_csv(output_path, index=False)

print(f"✓ Sample dataset created: {output_path}")
print(f"✓ Dataset shape: {df.shape}")
print(f"✓ Target distribution:")
print(df["target"].value_counts())
print("\nNote: This is a synthetic dataset for demonstration.")
print("For production use, download the real UCI Heart Disease dataset.")
