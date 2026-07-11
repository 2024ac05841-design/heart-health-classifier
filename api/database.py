"""
Redis database configuration and connection management
"""

import redis
import os
import logging
import json
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Redis connection URL
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Global Redis connection pool
redis_pool = None
redis_client = None


def init_redis():
    """
    Initialize Redis connection pool
    Call this on application startup
    """
    global redis_pool, redis_client

    try:
        # Create connection pool for better performance
        redis_pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,  # Automatically decode bytes to strings
            max_connections=50,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        # Create Redis client
        redis_client = redis.Redis(connection_pool=redis_pool)

        # Test connection
        redis_client.ping()

        logger.info(f"Redis initialized successfully at {REDIS_HOST}:{REDIS_PORT}")

        # Initialize auto-incrementing counter for prediction IDs if not exists
        if not redis_client.exists("prediction:id:counter"):
            redis_client.set("prediction:id:counter", 0)

    except Exception as e:
        logger.error(f"Failed to initialize Redis: {e}")
        raise


def get_redis() -> redis.Redis:
    """
    Get Redis client instance

    Usage in FastAPI endpoints:
        @app.get("/endpoint")
        def endpoint(db: redis.Redis = Depends(get_redis)):
            ...
    """
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client


def close_redis():
    """
    Close Redis connection pool
    Call this on application shutdown
    """
    global redis_pool, redis_client

    if redis_client:
        redis_client.close()
        redis_client = None

    if redis_pool:
        redis_pool.disconnect()
        redis_pool = None

    logger.info("Redis connection closed")
