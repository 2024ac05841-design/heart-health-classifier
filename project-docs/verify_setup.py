"""
Project Verification Script
Checks that all components are properly set up
"""

import os
import sys
from pathlib import Path


def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False


def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}/")
        return True
    else:
        print(f"❌ {description}: {dirpath}/ NOT FOUND")
        return False


def check_module(module_name):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ Module: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ Module: {module_name} - {str(e)}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 70)
    print("  Heart Disease MLOps Project - Verification")
    print("=" * 70)
    print()

    checks_passed = 0
    checks_total = 0

    # Check directories
    print("📁 Checking Directory Structure...")
    print("-" * 70)
    directories = [
        ("data/raw", "Data directory"),
        ("models", "Models directory"),
        ("src", "Source code"),
        ("api", "API code"),
        ("tests", "Tests"),
        ("scripts", "Scripts"),
        ("k8s", "Kubernetes configs"),
        (".github/workflows", "CI/CD workflows"),
    ]

    for dirpath, desc in directories:
        checks_total += 1
        if check_directory(dirpath, desc):
            checks_passed += 1

    print()

    # Check key files
    print("📄 Checking Key Files...")
    print("-" * 70)
    files = [
        ("requirements.txt", "Requirements file"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose"),
        ("README.md", "Main documentation"),
        (".gitignore", "Git ignore"),
        ("pytest.ini", "Pytest config"),
        ("api/app.py", "FastAPI application"),
        ("src/data_processing.py", "Data processing"),
        ("src/model_training.py", "Model training"),
        ("scripts/train_model.py", "Training script"),
        ("k8s/deployment.yaml", "K8s deployment"),
        (".github/workflows/ci-cd.yml", "CI/CD pipeline"),
    ]

    for filepath, desc in files:
        checks_total += 1
        if check_file(filepath, desc):
            checks_passed += 1

    print()

    # Check data and models
    print("📊 Checking Data and Models...")
    print("-" * 70)

    checks_total += 1
    if os.path.exists("data/raw/heart_disease.csv"):
        import pandas as pd

        try:
            df = pd.read_csv("data/raw/heart_disease.csv")
            print(f"✅ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
            checks_passed += 1
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
    else:
        print("❌ Dataset not found: data/raw/heart_disease.csv")

    checks_total += 1
    if os.path.exists("models/best_model.pkl"):
        print("✅ Trained model found: models/best_model.pkl")
        checks_passed += 1
    else:
        print("⚠️  Model not found (run: python scripts/train_model.py)")

    print()

    # Check Python modules
    print("🐍 Checking Python Dependencies...")
    print("-" * 70)
    modules = [
        "pandas",
        "numpy",
        "sklearn",
        "mlflow",
        "fastapi",
        "uvicorn",
        "pytest",
        "joblib",
    ]

    for module in modules:
        checks_total += 1
        if check_module(module):
            checks_passed += 1

    print()

    # Check API
    print("🚀 Checking API...")
    print("-" * 70)
    checks_total += 1
    try:
        from api.app import app

        print("✅ API module imports successfully")
        checks_passed += 1
    except Exception as e:
        print(f"❌ API import error: {e}")

    print()

    # Summary
    print("=" * 70)
    print(f"  Verification Results: {checks_passed}/{checks_total} checks passed")
    print("=" * 70)

    percentage = (checks_passed / checks_total) * 100

    if percentage == 100:
        print("✅ All checks passed! Project is fully set up.")
        print("\n📝 Next steps:")
        print("   1. Review README.md for documentation")
        print("   2. Run: python scripts/train_model.py (if model not found)")
        print("   3. Run: uvicorn api.app:app --reload")
        print("   4. Visit: http://localhost:8000/docs")
        return 0
    elif percentage >= 80:
        print("⚠️  Most checks passed. Review errors above.")
        print("\n📝 Common fixes:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Generate data: python data/create_sample_data.py")
        print("   - Train model: python scripts/train_model.py")
        return 1
    else:
        print("❌ Many checks failed. Please review errors above.")
        print("\n📝 Setup steps:")
        print("   1. Create venv: python -m venv venv")
        print("   2. Activate: .\\venv\\Scripts\\Activate.ps1")
        print("   3. Install: pip install -r requirements.txt")
        print("   4. Generate data: python data/create_sample_data.py")
        print("   5. Train model: python scripts/train_model.py")
        return 2


if __name__ == "__main__":
    sys.exit(main())
