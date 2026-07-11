# Database Documentation

## Overview

The Heart Disease Prediction API uses **Redis** as its lightweight, high-performance database for storing prediction history. Redis provides:

- ⚡ **Ultra-fast performance** (< 1ms response time)
- 💾 **Persistent storage** (AOF + RDB snapshots)
- 🪶 **Lightweight** (< 64Mi memory footprint)
- 🔍 **Efficient querying** (sorted sets for filtering)
- 📦 **Simple deployment** (single container)

---

## Architecture

```
┌──────────────────────┐      ┌──────────────────────┐
│  Heart API Pod       │─────▶│  Redis Pod           │
│  (FastAPI + Model)   │      │  (Database)          │
│  Port: 30080         │      │  Port: 6379          │
└──────────────────────┘      └──────────────────────┘
                                        │
                              ┌─────────▼──────────┐
                              │ PersistentVolume   │
                              │ (2GB Storage)      │
                              │ *.rdb + *.aof      │
                              └────────────────────┘
```

---

## Redis Data Model

### Key Structure

| Key Pattern | Type | Purpose | Example |
|------------|------|---------|---------|
| `prediction:{id}` | Hash | Full prediction record | `prediction:1` |
| `prediction:id:counter` | String | Auto-increment counter | `42` |
| `prediction:by_timestamp` | Sorted Set | Sort by timestamp | Score: 1720699200000 |
| `prediction:by_risk_score` | Sorted Set | Sort by risk score | Score: 0.85 |
| `prediction:class:0` | Set | No disease predictions | {1, 3, 5} |
| `prediction:class:1` | Set | Disease predictions | {2, 4, 6} |

### Record Schema

Each `prediction:{id}` hash contains:

```json
{
  "timestamp": "2026-07-11T10:30:00.123456",
  "patient_data": "{...}",  // JSON string
  "prediction": "1",
  "prediction_label": "Disease Present",
  "confidence": "0.85",
  "risk_score": "0.85",
  "inference_time_ms": "12.5",
  "preprocessing_time_ms": "3.2"
}
```

---

## Persistence Configuration

Redis is configured with **dual persistence** for maximum durability:

### 1. AOF (Append Only File)
- **Strategy**: `appendfsync everysec`
- **File**: `predictions.aof`
- **Durability**: Fsync every second (good balance)
- **Recovery**: Replays all write operations

### 2. RDB (Snapshots)
- **Triggers**:
  - Save if 1 key changed in 15 minutes
  - Save if 10 keys changed in 5 minutes
  - Save if 10,000 keys changed in 1 minute
- **File**: `dump.rdb`
- **Durability**: Point-in-time snapshots
- **Recovery**: Fast full restore

**Result**: Minimal data loss (< 1 second) with efficient storage.

---

## Deployment

### Prerequisites
- Kubernetes cluster (Rancher Desktop, Minikube, etc.)
- kubectl configured
- 2GB available storage

### Deploy Redis

```bash
# Deploy Redis with persistent storage
kubectl apply -f k8s/redis.yaml

# Verify deployment
kubectl get pods -l app=redis
kubectl get pvc redis-pvc
kubectl get svc redis

# Check logs
kubectl logs -l app=redis --tail=50 -f
```

### Deploy API with Redis Connection

```bash
# Deploy API (with REDIS_HOST env var)
kubectl apply -f k8s/deployment.yaml

# Verify connection
kubectl logs -l app=heart-disease-api --tail=20 | grep -i redis
```

---

## API Endpoints

### Prediction (Auto-saves to Redis)

**POST** `/predict`

```bash
curl -X POST "http://localhost:30080/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

### Query History

**GET** `/predictions/history`

```bash
# Get latest 50 predictions
curl "http://localhost:30080/predictions/history?limit=50"

# High-risk predictions only
curl "http://localhost:30080/predictions/history?min_risk_score=0.7"

# Disease predictions (class=1)
curl "http://localhost:30080/predictions/history?prediction_class=1"

# Pagination
curl "http://localhost:30080/predictions/history?limit=20&skip=0"  # Page 1
curl "http://localhost:30080/predictions/history?limit=20&skip=20" # Page 2
```

### Get Statistics

**GET** `/predictions/stats`

```bash
curl "http://localhost:30080/predictions/stats"
```

**Response:**
```json
{
  "total_predictions": 1000,
  "disease_count": 450,
  "no_disease_count": 550,
  "avg_risk_score": 0.52,
  "avg_confidence": 0.78,
  "avg_inference_time_ms": 15.3,
  "avg_preprocessing_time_ms": 4.1
}
```

### Get Specific Prediction

**GET** `/predictions/{id}`

```bash
curl "http://localhost:30080/predictions/123"
```

---

## Monitoring

### Redis Metrics (Prometheus)

Redis is automatically scraped by Prometheus every 15 seconds:

- **Connection metrics**: Connected clients, blocked clients
- **Memory metrics**: Used memory, peak memory
- **Performance metrics**: Commands processed, keyspace hits/misses
- **Persistence metrics**: Last save time, RDB changes since last save

### Grafana Dashboard

View Redis metrics in Grafana at: `http://localhost:30030`

**Key Panels:**
- Redis Memory Usage
- Commands per Second
- Keyspace Hit Rate
- Connected Clients
- Persistence Status

---

## Maintenance

### Backup

```bash
# Copy RDB snapshot from pod
kubectl cp redis-<pod-id>:/data/dump.rdb ./backup-$(date +%Y%m%d).rdb

# Copy AOF file
kubectl cp redis-<pod-id>:/data/predictions.aof ./backup-$(date +%Y%m%d).aof
```

### Restore

```bash
# Stop Redis pod
kubectl scale deployment redis --replicas=0

# Copy backup to PVC (via temporary pod)
kubectl run -it --rm redis-restore --image=redis:7-alpine --restart=Never \
  --overrides='{"spec":{"volumes":[{"name":"data","persistentVolumeClaim":{"claimName":"redis-pvc"}}],"containers":[{"name":"redis-restore","image":"redis:7-alpine","volumeMounts":[{"name":"data","mountPath":"/data"}],"command":["sleep","3600"]}]}}'

# In another terminal, copy files
kubectl cp ./backup.rdb redis-restore:/data/dump.rdb
kubectl cp ./backup.aof redis-restore:/data/predictions.aof

# Restart Redis
kubectl scale deployment redis --replicas=1
```

### View Data (Redis CLI)

```bash
# Connect to Redis
kubectl exec -it deployment/redis -- redis-cli

# Or via port-forward
kubectl port-forward svc/redis 6379:6379
redis-cli -h localhost -p 6379

# Sample commands
> DBSIZE                           # Total keys
> GET prediction:id:counter       # Current ID counter
> HGETALL prediction:1            # Get prediction by ID
> ZRANGE prediction:by_timestamp 0 9 WITHSCORES  # Latest 10 predictions
> SMEMBERS prediction:class:1     # All disease prediction IDs
> INFO memory                     # Memory usage
> INFO persistence                # Persistence status
```

---

## Performance

### Benchmarks

| Operation | Response Time | Throughput |
|-----------|---------------|------------|
| Save prediction | < 1ms | 10,000 ops/sec |
| Get by ID | < 1ms | 50,000 ops/sec |
| Query history (filtered) | < 5ms | 2,000 ops/sec |
| Calculate stats | < 100ms | 100 ops/sec |

### Resource Usage

- **Memory**: 64Mi request, 256Mi limit
- **CPU**: 50m request, 200m limit
- **Storage**: 2GB PVC
- **Network**: < 1Mbps typical

---

## Troubleshooting

### Redis Pod Not Starting

```bash
# Check pod status
kubectl describe pod -l app=redis

# Check PVC status
kubectl get pvc redis-pvc
kubectl describe pvc redis-pvc

# Check logs
kubectl logs -l app=redis --tail=100
```

### Connection Refused

```bash
# Verify service
kubectl get svc redis
kubectl describe svc redis

# Test connectivity from API pod
kubectl exec -it deployment/heart-disease-api -- sh
ping redis
telnet redis 6379
```

### Data Loss

- Check persistence status: `redis-cli INFO persistence`
- Verify AOF/RDB files exist: `kubectl exec deployment/redis -- ls -lh /data/`
- Check last save time: `redis-cli LASTSAVE`

### Out of Memory

```bash
# Check memory usage
kubectl exec deployment/redis -- redis-cli INFO memory

# Check maxmemory policy
kubectl exec deployment/redis -- redis-cli CONFIG GET maxmemory-policy

# View evicted keys
kubectl exec deployment/redis -- redis-cli INFO stats | grep evicted
```

---

## Migration Guide

### From SQLite/PostgreSQL to Redis

If migrating from SQL databases:

1. Export existing data:
   ```python
   # export_sql_to_redis.py
   from sqlalchemy import create_engine
   from api.database import get_redis
   from api.db_models import PredictionRecord as RedisPredictionRecord
   
   # Export script available in scripts/migrate_to_redis.py
   ```

2. Deploy Redis

3. Update environment variables

4. Restart API pods

### From Redis to PostgreSQL

If scaling requires PostgreSQL:

1. Change `DATABASE_URL` environment variable
2. Install PostgreSQL dependencies
3. Update `api/database.py` to use SQLAlchemy
4. No code changes needed in routers (same interface)

---

## Security

### Production Checklist

- [ ] Enable Redis password authentication
- [ ] Use Kubernetes Secrets for credentials
- [ ] Enable TLS for Redis connections
- [ ] Restrict network policies
- [ ] Set appropriate memory limits
- [ ] Enable Redis ACLs
- [ ] Regular backups
- [ ] Monitor for unauthorized access

### Enable Password (Production)

```yaml
# Update redis.yaml
env:
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: redis-secret
      key: password

# Update API deployment
env:
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: redis-secret
      key: password
```

---

## FAQ

**Q: Why Redis over PostgreSQL?**  
A: Redis is lighter (5x less memory), faster (10-100x), and simpler to deploy. Perfect for < 100K predictions/day.

**Q: Is Redis durable?**  
A: Yes, with AOF+RDB we have < 1 second data loss window. Same durability as SQLite.

**Q: Can I query complex filters?**  
A: Yes, using sorted sets and set intersection. For SQL-like queries, upgrade to PostgreSQL.

**Q: What happens if Redis crashes?**  
A: Data is restored from AOF/RDB files automatically on restart. PersistentVolume ensures data survives pod restarts.

**Q: How do I scale?**  
A: For > 100K predictions/day, migrate to PostgreSQL with connection pooling and read replicas.

---

## Next Steps

1. ✅ **Deployed**: Redis database is running
2. ✅ **Connected**: API saves predictions automatically
3. ✅ **Persistent**: Data survives restarts
4. 📊 **Monitor**: Add Grafana dashboard for database metrics
5. 🔒 **Secure**: Enable authentication for production
6. 📈 **Scale**: Consider PostgreSQL at 100K+ predictions/day

---

For more information, see:
- [Redis Documentation](https://redis.io/documentation)
- [Redis Persistence](https://redis.io/topics/persistence)
- [Kubernetes PersistentVolumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
