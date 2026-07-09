"""
Test the deployed API
"""

import requests
import json

# API endpoint (change to your deployed URL)
API_URL = "http://localhost:8000"

# Sample patient data
sample_patient = {
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1,
}


def test_root():
    """Test root endpoint"""
    print("\n" + "=" * 60)
    print("Testing Root Endpoint")
    print("=" * 60)

    response = requests.get(f"{API_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 60)
    print("Testing Health Check Endpoint")
    print("=" * 60)

    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_predict():
    """Test prediction endpoint"""
    print("\n" + "=" * 60)
    print("Testing Prediction Endpoint")
    print("=" * 60)

    print(f"\nInput Data:")
    print(json.dumps(sample_patient, indent=2))

    response = requests.post(f"{API_URL}/predict", json=sample_patient)
    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nPrediction Result:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")


def test_model_info():
    """Test model info endpoint"""
    print("\n" + "=" * 60)
    print("Testing Model Info Endpoint")
    print("=" * 60)

    response = requests.get(f"{API_URL}/model/info")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  Heart Disease Prediction API - Testing Suite")
    print("=" * 70)
    print(f"API URL: {API_URL}")

    try:
        test_root()
        test_health()
        test_model_info()
        test_predict()

        print("\n" + "=" * 70)
        print("  All Tests Completed!")
        print("=" * 70)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print(f"Please ensure the API is running at {API_URL}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
