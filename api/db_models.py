"""
Redis data models and helper functions for storing predictions
"""

import json
from datetime import datetime
from typing import Dict, Optional, Any
import redis


class PredictionRecord:
    """
    Model for storing prediction records in Redis

    Redis Key Structure:
    - request:{id} -> Hash with all fields
    - request:id:counter -> Auto-incrementing ID counter
    - request:by_timestamp -> Sorted Set (timestamp as score)
    - request:by_risk_score -> Sorted Set (risk_score as score)
    - request:class:{0|1} -> Set of request IDs by class

    Schema:
    - id: Unique prediction ID
    - timestamp: ISO format timestamp
    - patient_data: JSON string with input features
    - prediction: 0 or 1
    - prediction_label: "Disease Present" or "No Disease"
    - confidence: Float (0.0-1.0)
    - risk_score: Float (0.0-1.0)
    - inference_time_ms: Float
    - preprocessing_time_ms: Float
    """

    def __init__(
        self,
        patient_data: Dict[str, Any],
        prediction: int,
        prediction_label: str,
        confidence: float,
        risk_score: float,
        inference_time_ms: Optional[float] = None,
        preprocessing_time_ms: Optional[float] = None,
        id: Optional[int] = None,
        timestamp: Optional[str] = None,
    ):
        self.id = id
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.patient_data = patient_data
        self.prediction = prediction
        self.prediction_label = prediction_label
        self.confidence = confidence
        self.risk_score = risk_score
        self.inference_time_ms = inference_time_ms
        self.preprocessing_time_ms = preprocessing_time_ms

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "patient_data": self.patient_data,
            "prediction": self.prediction,
            "prediction_label": self.prediction_label,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "inference_time_ms": self.inference_time_ms,
            "preprocessing_time_ms": self.preprocessing_time_ms,
        }

    def to_redis_hash(self) -> Dict[str, str]:
        """Convert record to Redis hash format (all strings)"""
        return {
            "timestamp": self.timestamp,
            "patient_data": json.dumps(self.patient_data),
            "prediction": str(self.prediction),
            "prediction_label": self.prediction_label,
            "confidence": str(self.confidence),
            "risk_score": str(self.risk_score),
            "inference_time_ms": (
                str(self.inference_time_ms) if self.inference_time_ms else ""
            ),
            "preprocessing_time_ms": (
                str(self.preprocessing_time_ms) if self.preprocessing_time_ms else ""
            ),
        }

    @classmethod
    def from_redis_hash(cls, id: int, redis_hash: Dict[str, str]) -> "PredictionRecord":
        """Create PredictionRecord from Redis hash"""
        return cls(
            id=id,
            timestamp=redis_hash.get("timestamp"),
            patient_data=json.loads(redis_hash.get("patient_data", "{}")),
            prediction=int(redis_hash.get("prediction", 0)),
            prediction_label=redis_hash.get("prediction_label", ""),
            confidence=float(redis_hash.get("confidence", 0.0)),
            risk_score=float(redis_hash.get("risk_score", 0.0)),
            inference_time_ms=(
                float(redis_hash.get("inference_time_ms"))
                if redis_hash.get("inference_time_ms")
                else None
            ),
            preprocessing_time_ms=(
                float(redis_hash.get("preprocessing_time_ms"))
                if redis_hash.get("preprocessing_time_ms")
                else None
            ),
        )

    def save(self, redis_client: redis.Redis) -> int:
        """
        Save prediction record to Redis

        Returns:
            int: The ID of the saved prediction
        """
        # Generate new ID
        prediction_id = redis_client.incr("request:id:counter")
        self.id = prediction_id

        # Save to Redis hash
        key = f"request:{prediction_id}"
        redis_client.hset(key, mapping=self.to_redis_hash())

        # Add to sorted sets for efficient querying
        timestamp_ms = datetime.fromisoformat(self.timestamp).timestamp() * 1000
        redis_client.zadd("request:by_timestamp", {prediction_id: timestamp_ms})
        redis_client.zadd("request:by_risk_score", {prediction_id: self.risk_score})

        # Add to set by prediction class
        redis_client.sadd(f"request:class:{self.prediction}", prediction_id)

        # Set expiry if needed (optional - e.g., 90 days)
        # redis_client.expire(key, 90 * 24 * 60 * 60)

        return prediction_id

    @classmethod
    def get_by_id(
        cls, redis_client: redis.Redis, prediction_id: int
    ) -> Optional["PredictionRecord"]:
        """Get prediction record by ID"""
        key = f"request:{prediction_id}"
        redis_hash = redis_client.hgetall(key)

        if not redis_hash:
            return None

        return cls.from_redis_hash(prediction_id, redis_hash)

    @classmethod
    def get_latest(
        cls,
        redis_client: redis.Redis,
        limit: int = 100,
        skip: int = 0,
        prediction_class: Optional[int] = None,
        min_risk_score: Optional[float] = None,
        max_risk_score: Optional[float] = None,
    ) -> list["PredictionRecord"]:
        """
        Get latest predictions with optional filtering

        Args:
            redis_client: Redis client instance
            limit: Maximum number of records to return
            skip: Number of records to skip (pagination)
            prediction_class: Filter by prediction class (0 or 1)
            min_risk_score: Minimum risk score filter
            max_risk_score: Maximum risk score filter

        Returns:
            List of PredictionRecord objects
        """
        # Start with all IDs sorted by timestamp (newest first)
        all_ids = redis_client.zrevrange("request:by_timestamp", 0, -1)

        # Apply filters
        filtered_ids = []

        for pred_id in all_ids:
            pred_id = int(pred_id)

            # Filter by prediction class
            if prediction_class is not None:
                if not redis_client.sismember(
                    f"request:class:{prediction_class}", pred_id
                ):
                    continue

            # Filter by risk score
            if min_risk_score is not None or max_risk_score is not None:
                risk_score = redis_client.zscore("request:by_risk_score", pred_id)
                if risk_score is None:
                    continue
                if min_risk_score is not None and risk_score < min_risk_score:
                    continue
                if max_risk_score is not None and risk_score > max_risk_score:
                    continue

            filtered_ids.append(pred_id)

        # Apply pagination
        paginated_ids = filtered_ids[skip : skip + limit]

        # Fetch full records
        records = []
        for pred_id in paginated_ids:
            record = cls.get_by_id(redis_client, pred_id)
            if record:
                records.append(record)

        return records

    @classmethod
    def get_statistics(cls, redis_client: redis.Redis) -> Dict[str, Any]:
        """
        Calculate statistics for all predictions

        Returns:
            Dictionary with aggregated statistics
        """
        # Get total count
        total = redis_client.get("request:id:counter")
        total = int(total) if total else 0

        if total == 0:
            return {
                "total_predictions": 0,
                "disease_count": 0,
                "no_disease_count": 0,
                "avg_risk_score": 0.0,
                "avg_confidence": 0.0,
                "avg_inference_time_ms": 0.0,
                "avg_preprocessing_time_ms": 0.0,
            }

        # Count by prediction class
        disease_count = redis_client.scard("request:class:1")
        no_disease_count = redis_client.scard("request:class:0")

        # Calculate averages (need to iterate through records)
        all_ids = redis_client.zrange("request:by_timestamp", 0, -1)

        total_risk = 0.0
        total_conf = 0.0
        total_inference = 0.0
        total_preprocessing = 0.0
        inference_count = 0
        preprocessing_count = 0

        for pred_id in all_ids:
            record = cls.get_by_id(redis_client, int(pred_id))
            if record:
                total_risk += record.risk_score
                total_conf += record.confidence
                if record.inference_time_ms:
                    total_inference += record.inference_time_ms
                    inference_count += 1
                if record.preprocessing_time_ms:
                    total_preprocessing += record.preprocessing_time_ms
                    preprocessing_count += 1

        return {
            "total_predictions": total,
            "disease_count": disease_count,
            "no_disease_count": no_disease_count,
            "avg_risk_score": round(total_risk / total, 4) if total > 0 else 0.0,
            "avg_confidence": round(total_conf / total, 4) if total > 0 else 0.0,
            "avg_inference_time_ms": (
                round(total_inference / inference_count, 2)
                if inference_count > 0
                else 0.0
            ),
            "avg_preprocessing_time_ms": (
                round(total_preprocessing / preprocessing_count, 2)
                if preprocessing_count > 0
                else 0.0
            ),
        }
