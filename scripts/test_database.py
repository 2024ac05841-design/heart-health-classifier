"""
Test script to verify Redis database integration

Usage:
    python scripts/test_database.py
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:30080"

# Test patient data
HIGH_RISK_PATIENT = {
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

LOW_RISK_PATIENT = {
    "age": 45,
    "sex": 0,
    "cp": 0,
    "trestbps": 110,
    "chol": 180,
    "fbs": 0,
    "restecg": 0,
    "thalach": 170,
    "exang": 0,
    "oldpeak": 0.0,
    "slope": 0,
    "ca": 0,
    "thal": 0,
}


def test_prediction_and_storage():
    """Test that predictions are saved to Redis"""
    print("\n" + "=" * 60)
    print("TEST 1: Prediction with Redis Storage")
    print("=" * 60)

    # Make prediction
    response = requests.post(f"{BASE_URL}/predict", json=HIGH_RISK_PATIENT)

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Prediction successful:")
        print(f"   - Prediction: {result['prediction_label']}")
        print(f"   - Confidence: {result['confidence']:.2f}")
        print(f"   - Risk Score: {result['risk_score']:.2f}")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(response.text)
        return False

    return True


def test_get_history():
    """Test retrieving prediction history"""
    print("\n" + "=" * 60)
    print("TEST 2: Get Prediction History")
    print("=" * 60)

    # Wait a moment for data to be persisted
    time.sleep(1)

    # Get history
    response = requests.get(f"{BASE_URL}/predictions/history?limit=10")

    if response.status_code == 200:
        records = response.json()
        print(f"✅ Retrieved {len(records)} prediction records")

        if records:
            latest = records[0]
            print(f"\nLatest prediction:")
            print(f"   - ID: {latest['id']}")
            print(f"   - Timestamp: {latest['timestamp']}")
            print(f"   - Prediction: {latest['prediction_label']}")
            print(f"   - Risk Score: {latest['risk_score']:.2f}")
            return latest["id"]
    else:
        print(f"❌ Failed to retrieve history: {response.status_code}")
        print(response.text)

    return None


def test_get_by_id(prediction_id: int):
    """Test retrieving specific prediction by ID"""
    print("\n" + "=" * 60)
    print(f"TEST 3: Get Prediction by ID ({prediction_id})")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/predictions/{prediction_id}")

    if response.status_code == 200:
        record = response.json()
        print(f"✅ Retrieved prediction {prediction_id}:")
        print(f"   - Timestamp: {record['timestamp']}")
        print(f"   - Prediction: {record['prediction_label']}")
        print(f"   - Patient Age: {record['patient_data']['age']}")
        print(f"   - Inference Time: {record['inference_time_ms']:.2f}ms")
    else:
        print(f"❌ Failed to retrieve prediction: {response.status_code}")
        print(response.text)
        return False

    return True


def test_get_statistics():
    """Test retrieving prediction statistics"""
    print("\n" + "=" * 60)
    print("TEST 4: Get Prediction Statistics")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/predictions/stats")

    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Statistics retrieved:")
        print(f"   - Total Predictions: {stats['total_predictions']}")
        print(f"   - Disease Count: {stats['disease_count']}")
        print(f"   - No Disease Count: {stats['no_disease_count']}")
        print(f"   - Avg Risk Score: {stats['avg_risk_score']:.4f}")
        print(f"   - Avg Confidence: {stats['avg_confidence']:.4f}")
        print(f"   - Avg Inference Time: {stats['avg_inference_time_ms']:.2f}ms")
    else:
        print(f"❌ Failed to retrieve statistics: {response.status_code}")
        print(response.text)
        return False

    return True


def test_filtered_queries():
    """Test filtered queries"""
    print("\n" + "=" * 60)
    print("TEST 5: Filtered Queries")
    print("=" * 60)

    # Test 1: High risk predictions
    response = requests.get(
        f"{BASE_URL}/predictions/history?min_risk_score=0.7&limit=5"
    )
    if response.status_code == 200:
        high_risk = response.json()
        print(f"✅ High-risk predictions (risk > 0.7): {len(high_risk)} records")
    else:
        print(f"❌ High-risk query failed")
        return False

    # Test 2: Disease predictions only
    response = requests.get(
        f"{BASE_URL}/predictions/history?prediction_class=1&limit=5"
    )
    if response.status_code == 200:
        disease = response.json()
        print(f"✅ Disease predictions (class=1): {len(disease)} records")
    else:
        print(f"❌ Disease query failed")
        return False

    # Test 3: No disease predictions only
    response = requests.get(
        f"{BASE_URL}/predictions/history?prediction_class=0&limit=5"
    )
    if response.status_code == 200:
        no_disease = response.json()
        print(f"✅ No disease predictions (class=0): {len(no_disease)} records")
    else:
        print(f"❌ No disease query failed")
        return False

    return True


def test_multiple_predictions():
    """Test multiple predictions to populate database"""
    print("\n" + "=" * 60)
    print("TEST 6: Multiple Predictions (Population Test)")
    print("=" * 60)

    success_count = 0
    total = 5

    for i in range(total):
        # Alternate between high and low risk patients
        patient = HIGH_RISK_PATIENT if i % 2 == 0 else LOW_RISK_PATIENT
        response = requests.post(f"{BASE_URL}/predict", json=patient)

        if response.status_code == 200:
            success_count += 1

        time.sleep(0.1)  # Small delay between requests

    print(f"✅ Successfully created {success_count}/{total} predictions")
    return success_count == total


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🔬 Redis Database Integration Tests")
    print("=" * 60)
    print(f"\nTesting API at: {BASE_URL}")

    # Check if API is accessible
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API health check failed!")
            print("   Make sure the API is running: kubectl get pods")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {BASE_URL}")
        print("   Make sure:")
        print("   1. API pod is running: kubectl get pods")
        print(
            "   2. Port-forward is active: kubectl port-forward svc/heart-disease-api-service 30080:80"
        )
        print("   Or access via NodePort: http://localhost:30080")
        return

    print("✅ API is accessible\n")

    # Run tests
    results = []

    # Test 1: Basic prediction
    results.append(("Prediction with Storage", test_prediction_and_storage()))

    # Test 2: Multiple predictions
    results.append(("Multiple Predictions", test_multiple_predictions()))

    # Test 3: Get history
    prediction_id = test_get_history()
    results.append(("Get History", prediction_id is not None))

    # Test 4: Get by ID
    if prediction_id:
        results.append(("Get by ID", test_get_by_id(prediction_id)))

    # Test 5: Statistics
    results.append(("Get Statistics", test_get_statistics()))

    # Test 6: Filtered queries
    results.append(("Filtered Queries", test_filtered_queries()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Redis database integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
