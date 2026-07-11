"""
Prediction history endpoints
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
import redis
from typing import List, Optional
import logging

from api.database import get_redis
from api.db_models import PredictionRecord
from api.models import PredictionHistoryResponse, PredictionRecordDetail

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/predictions/history",
    response_model=List[PredictionRecordDetail],
    summary="Get prediction history",
    description="Retrieve historical predictions with optional filtering",
    tags=["Prediction History"],
)
async def get_prediction_history(
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    skip: int = Query(
        0, ge=0, description="Number of records to skip (for pagination)"
    ),
    prediction_class: Optional[int] = Query(
        None, ge=0, le=1, description="Filter by prediction class (0 or 1)"
    ),
    min_risk_score: Optional[float] = Query(
        None, ge=0.0, le=1.0, description="Minimum risk score filter"
    ),
    max_risk_score: Optional[float] = Query(
        None, ge=0.0, le=1.0, description="Maximum risk score filter"
    ),
    db: redis.Redis = Depends(get_redis),
):
    """
    **Get Prediction History**

    Retrieve historical predictions with optional filtering and pagination.

    ### Query Parameters
    - **limit**: Maximum records to return (default: 100, max: 1000)
    - **skip**: Records to skip for pagination (default: 0)
    - **prediction_class**: Filter by prediction (0=No disease, 1=Disease)
    - **min_risk_score**: Filter by minimum risk score (0.0-1.0)
    - **max_risk_score**: Filter by maximum risk score (0.0-1.0)
    - **days_back**: Only show predictions from last N days

    ### Returns
    List of prediction records with:
    - ID and timestamp
    - Input patient data
    - Prediction results (class, label, confidence, risk score)
    - Performance metrics (inference time, preprocessing time)

    ### Example Usage
    - Get last 50 high-risk predictions: `?limit=50&min_risk_score=0.7`
    - Get disease predictions: `?prediction_class=1`
    - Pagination: First page `?limit=20&skip=0`, second page `?limit=20&skip=20`
    """
    try:
        # Get filtered records from Redis
        records = PredictionRecord.get_latest(
            redis_client=db,
            limit=limit,
            skip=skip,
            prediction_class=prediction_class,
            min_risk_score=min_risk_score,
            max_risk_score=max_risk_score,
        )

        logger.info(f"Retrieved {len(records)} prediction records")

        # Convert to response format
        return [record.to_dict() for record in records]
    except Exception as e:
        logger.error(f"Error retrieving prediction history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve prediction history: {str(e)}",
        )


@router.get(
    "/predictions/stats",
    response_model=PredictionHistoryResponse,
    summary="Get prediction statistics",
    description="Get summary statistics of all predictions",
    tags=["Prediction History"],
)
async def get_prediction_stats(
    db: redis.Redis = Depends(get_redis),
):
    """
    **Get Prediction Statistics**

    Get summary statistics for all predictions in Redis.

    ### Statistics Included
    - Total number of predictions
    - Count by prediction class (disease vs no disease)
    - Average risk score
    - Average confidence
    - Average inference and preprocessing times

    ### Returns
    Aggregated statistics for all predictions
    """
    try:
        stats = PredictionRecord.get_statistics(redis_client=db)
        logger.info(
            f"Calculated statistics for {stats['total_predictions']} predictions"
        )
        return stats

    except Exception as e:
        logger.error(f"Error calculating prediction statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate statistics: {str(e)}",
        )


@router.get(
    "/predictions/{prediction_id}",
    response_model=PredictionRecordDetail,
    summary="Get specific prediction by ID",
    description="Retrieve a single prediction record by its ID",
    tags=["Prediction History"],
)
async def get_prediction_by_id(
    prediction_id: int,
    db: redis.Redis = Depends(get_redis),
):
    """
    **Get Prediction by ID**

    Retrieve a specific prediction record by its Redis ID.

    ### Path Parameters
    - **prediction_id**: The unique ID of the prediction record

    ### Returns
    Complete prediction record including input data and results
    """
    try:
        record = PredictionRecord.get_by_id(
            redis_client=db, prediction_id=prediction_id
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID {prediction_id} not found",
            )

        logger.info(f"Retrieved prediction record ID: {prediction_id}")
        return record.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving prediction {prediction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve prediction: {str(e)}",
        )
