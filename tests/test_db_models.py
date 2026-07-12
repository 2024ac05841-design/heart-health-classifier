"""
Unit tests for Redis database models
"""

import pytest
import json
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from api.db_models import PredictionRecord


class TestPredictionRecord:
    """Test suite for PredictionRecord model"""

    @pytest.fixture
    def sample_patient_data(self):
        """Create sample patient data"""
        return {
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

    @pytest.fixture
    def sample_record(self, sample_patient_data):
        """Create sample PredictionRecord"""
        return PredictionRecord(
            patient_data=sample_patient_data,
            prediction=1,
            prediction_label="Disease Present",
            confidence=0.85,
            risk_score=0.72,
            inference_time_ms=12.5,
            preprocessing_time_ms=3.2,
            id=1,
            timestamp="2024-01-15T10:30:00",
        )

    @pytest.fixture
    def mock_redis_client(self):
        """Create mock Redis client"""
        redis_mock = Mock()
        redis_mock.incr = Mock(return_value=1)
        redis_mock.hset = Mock(return_value=True)
        redis_mock.zadd = Mock(return_value=1)
        redis_mock.sadd = Mock(return_value=1)
        redis_mock.hgetall = Mock(return_value={})
        redis_mock.zrevrange = Mock(return_value=[])
        redis_mock.zrange = Mock(return_value=[])
        redis_mock.sismember = Mock(return_value=True)
        redis_mock.zscore = Mock(return_value=0.5)
        redis_mock.get = Mock(return_value=b"10")
        redis_mock.scard = Mock(return_value=5)
        return redis_mock

    def test_prediction_record_init(self, sample_patient_data):
        """Test PredictionRecord initialization"""
        record = PredictionRecord(
            patient_data=sample_patient_data,
            prediction=1,
            prediction_label="Disease Present",
            confidence=0.85,
            risk_score=0.72,
        )

        assert record.patient_data == sample_patient_data
        assert record.prediction == 1
        assert record.prediction_label == "Disease Present"
        assert record.confidence == 0.85
        assert record.risk_score == 0.72
        assert record.timestamp is not None
        assert record.id is None

    def test_prediction_record_with_optional_fields(self, sample_patient_data):
        """Test PredictionRecord with all optional fields"""
        record = PredictionRecord(
            patient_data=sample_patient_data,
            prediction=0,
            prediction_label="No Disease",
            confidence=0.92,
            risk_score=0.15,
            inference_time_ms=10.5,
            preprocessing_time_ms=2.3,
            id=42,
            timestamp="2024-01-15T10:30:00",
        )

        assert record.id == 42
        assert record.timestamp == "2024-01-15T10:30:00"
        assert record.inference_time_ms == 10.5
        assert record.preprocessing_time_ms == 2.3

    def test_to_dict(self, sample_record):
        """Test converting record to dictionary"""
        record_dict = sample_record.to_dict()

        assert isinstance(record_dict, dict)
        assert record_dict["id"] == 1
        assert record_dict["prediction"] == 1
        assert record_dict["prediction_label"] == "Disease Present"
        assert record_dict["confidence"] == 0.85
        assert record_dict["risk_score"] == 0.72
        assert record_dict["inference_time_ms"] == 12.5
        assert record_dict["preprocessing_time_ms"] == 3.2
        assert "timestamp" in record_dict
        assert "patient_data" in record_dict

    def test_to_redis_hash(self, sample_record):
        """Test converting record to Redis hash format"""
        redis_hash = sample_record.to_redis_hash()

        assert isinstance(redis_hash, dict)
        assert redis_hash["prediction"] == "1"
        assert redis_hash["prediction_label"] == "Disease Present"
        assert redis_hash["confidence"] == "0.85"
        assert redis_hash["risk_score"] == "0.72"
        assert redis_hash["inference_time_ms"] == "12.5"
        assert redis_hash["preprocessing_time_ms"] == "3.2"

        # Check patient_data is JSON string
        patient_data = json.loads(redis_hash["patient_data"])
        assert patient_data["age"] == 63

    def test_to_redis_hash_without_timing(self, sample_patient_data):
        """Test Redis hash conversion without timing data"""
        record = PredictionRecord(
            patient_data=sample_patient_data,
            prediction=0,
            prediction_label="No Disease",
            confidence=0.95,
            risk_score=0.1,
        )

        redis_hash = record.to_redis_hash()
        assert redis_hash["inference_time_ms"] == ""
        assert redis_hash["preprocessing_time_ms"] == ""

    def test_from_redis_hash(self, sample_patient_data):
        """Test creating PredictionRecord from Redis hash"""
        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }

        record = PredictionRecord.from_redis_hash(42, redis_hash)

        assert record.id == 42
        assert record.timestamp == "2024-01-15T10:30:00"
        assert record.prediction == 1
        assert record.confidence == 0.85
        assert record.risk_score == 0.72
        assert record.inference_time_ms == 12.5
        assert record.preprocessing_time_ms == 3.2
        assert record.patient_data["age"] == 63

    def test_from_redis_hash_without_timing(self):
        """Test creating record from Redis hash without timing data"""
        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": "{}",
            "prediction": "0",
            "prediction_label": "No Disease",
            "confidence": "0.95",
            "risk_score": "0.1",
            "inference_time_ms": "",
            "preprocessing_time_ms": "",
        }

        record = PredictionRecord.from_redis_hash(1, redis_hash)

        assert record.inference_time_ms is None
        assert record.preprocessing_time_ms is None

    def test_save(self, sample_record, mock_redis_client):
        """Test saving record to Redis"""
        mock_redis_client.incr.return_value = 123

        record_id = sample_record.save(mock_redis_client)

        assert record_id == 123
        assert sample_record.id == 123

        # Verify Redis operations were called
        mock_redis_client.incr.assert_called_once_with("request:id:counter")
        mock_redis_client.hset.assert_called_once()
        assert mock_redis_client.zadd.call_count == 2  # timestamp and risk_score
        mock_redis_client.sadd.assert_called_once()

    def test_get_by_id_found(self, mock_redis_client, sample_patient_data):
        """Test retrieving record by ID when found"""
        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }
        mock_redis_client.hgetall.return_value = redis_hash

        record = PredictionRecord.get_by_id(mock_redis_client, 42)

        assert record is not None
        assert record.id == 42
        assert record.prediction == 1
        mock_redis_client.hgetall.assert_called_once_with("request:42")

    def test_get_by_id_not_found(self, mock_redis_client):
        """Test retrieving non-existent record"""
        mock_redis_client.hgetall.return_value = {}

        record = PredictionRecord.get_by_id(mock_redis_client, 999)

        assert record is None

    def test_get_latest(self, mock_redis_client, sample_patient_data):
        """Test retrieving latest predictions"""
        # Mock Redis responses
        mock_redis_client.zrevrange.return_value = [b"1", b"2", b"3"]

        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }
        mock_redis_client.hgetall.return_value = redis_hash

        records = PredictionRecord.get_latest(mock_redis_client, limit=10)

        # Should return 3 records (mocked IDs: 1, 2, 3)
        assert len(records) == 3
        mock_redis_client.zrevrange.assert_called_once_with(
            "request:by_timestamp", 0, -1
        )

    def test_get_latest_with_filters(self, mock_redis_client):
        """Test retrieving predictions with filters"""
        mock_redis_client.zrevrange.return_value = [b"1", b"2", b"3"]
        mock_redis_client.sismember.return_value = True
        mock_redis_client.zscore.return_value = 0.5

        records = PredictionRecord.get_latest(
            mock_redis_client,
            limit=10,
            prediction_class=1,
            min_risk_score=0.4,
            max_risk_score=0.8,
        )

        # Verify filtering logic was called
        assert mock_redis_client.sismember.called
        assert mock_redis_client.zscore.called

    def test_get_latest_with_pagination(self, mock_redis_client, sample_patient_data):
        """Test pagination in get_latest"""
        mock_redis_client.zrevrange.return_value = [b"1", b"2", b"3", b"4", b"5"]

        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }
        mock_redis_client.hgetall.return_value = redis_hash

        # Skip first 2, limit 2
        records = PredictionRecord.get_latest(mock_redis_client, limit=2, skip=2)

        # Should return 2 records (IDs: 3, 4)
        assert len(records) == 2

    def test_get_statistics_with_data(self, mock_redis_client, sample_patient_data):
        """Test statistics calculation with data"""
        # Mock counter
        mock_redis_client.get.return_value = b"10"
        mock_redis_client.scard.side_effect = [6, 4]  # disease_count, no_disease_count
        mock_redis_client.zrange.return_value = [b"1", b"2"]

        # Mock record retrieval
        redis_hash = {
            "timestamp": "2024-01-15T10:30:00",
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }
        mock_redis_client.hgetall.return_value = redis_hash

        stats = PredictionRecord.get_statistics(mock_redis_client)

        assert stats["total_predictions"] == 10
        assert stats["disease_count"] == 6
        assert stats["no_disease_count"] == 4
        assert "avg_risk_score" in stats
        assert "avg_confidence" in stats

    def test_get_statistics_empty(self, mock_redis_client):
        """Test statistics calculation with no data"""
        mock_redis_client.get.return_value = None

        stats = PredictionRecord.get_statistics(mock_redis_client)

        assert stats["total_predictions"] == 0
        assert stats["disease_count"] == 0
        assert stats["no_disease_count"] == 0
        assert stats["avg_risk_score"] == 0.0
        assert stats["avg_confidence"] == 0.0

    def test_roundtrip_save_and_retrieve(self, mock_redis_client, sample_patient_data):
        """Test complete save and retrieve cycle"""
        # Create record
        record = PredictionRecord(
            patient_data=sample_patient_data,
            prediction=1,
            prediction_label="Disease Present",
            confidence=0.85,
            risk_score=0.72,
            inference_time_ms=12.5,
            preprocessing_time_ms=3.2,
        )

        # Mock save
        mock_redis_client.incr.return_value = 123
        record_id = record.save(mock_redis_client)

        assert record_id == 123
        assert record.id == 123

        # Mock retrieve
        redis_hash = {
            "timestamp": record.timestamp,
            "patient_data": json.dumps(sample_patient_data),
            "prediction": "1",
            "prediction_label": "Disease Present",
            "confidence": "0.85",
            "risk_score": "0.72",
            "inference_time_ms": "12.5",
            "preprocessing_time_ms": "3.2",
        }
        mock_redis_client.hgetall.return_value = redis_hash

        retrieved = PredictionRecord.get_by_id(mock_redis_client, 123)

        assert retrieved is not None
        assert retrieved.id == 123
        assert retrieved.prediction == record.prediction
        assert retrieved.confidence == record.confidence
        assert retrieved.risk_score == record.risk_score
