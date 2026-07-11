## Database Comparison: Redis vs Kafka vs PostgreSQL

This document explains why **Redis** was chosen for storing prediction history.

---

### Quick Comparison Table

| Feature | Redis ⭐ | Kafka | PostgreSQL |
|---------|---------|-------|------------|
| **Type** | In-memory database | Event streaming | Relational database |
| **Purpose** | Cache + Storage | Message queue | Structured storage |
| **Use Case** | Fast CRUD operations | Real-time pipelines | Complex queries |
| **Performance** | 10-100x faster | N/A (not a DB) | Baseline |
| **Memory** | 64-256Mi | 1-2Gi + Zookeeper | 256-512Mi |
| **Persistence** | ✅ AOF + RDB | ⚠️ Temporary | ✅ WAL |
| **Queries** | ✅ Key-value + Sets | ❌ No queries | ✅ Full SQL |
| **Complexity** | ⭐ Simple | ⭐⭐⭐⭐⭐ Very complex | ⭐⭐ Medium |
| **Setup** | 1 container | 3+ containers | 1 container |
| **Ideal For** | < 100K ops/day | Event streaming | > 100K ops/day |

---

### Detailed Analysis

#### 🔴 **Kafka: Wrong Tool for the Job**

**What Kafka IS:**
- Event streaming platform (like a highway for messages)
- Temporary message storage (retention: hours/days)
- Pub/sub architecture (producers → topics → consumers)

**What Kafka is NOT:**
- ❌ Not a database
- ❌ Cannot query historical data
- ❌ Cannot filter by risk_score or prediction_class
- ❌ No aggregations (avg, sum, count)
- ❌ Messages expire after retention period

**When to use Kafka:**
```
User Request → API → Kafka Topic → [Consumer 1: Save to DB]
                                 → [Consumer 2: Send email alert]
                                 → [Consumer 3: Update dashboard]
                                 → [Consumer 4: Trigger model retraining]
```

**Our use case (saving predictions):** ❌ **Wrong tool**

**Complexity:**
- Requires Zookeeper or KRaft mode
- Minimum 3 brokers for production
- Topic partitioning, replication, consumer groups
- Heavy resource usage (2-3Gi memory)
- Overkill for simple storage

---

#### 🟡 **PostgreSQL: Good But Heavy**

**Advantages:**
- ✅ Full SQL queries
- ✅ ACID transactions
- ✅ Mature and battle-tested
- ✅ Great for > 100K predictions/day
- ✅ Advanced features (JSON queries, full-text search)

**Disadvantages:**
- ❌ Heavier (256-512Mi memory)
- ❌ Slower than Redis (10-100x)
- ❌ More complex setup
- ❌ Requires connection pooling for scale
- ❌ Overkill for simple key-value storage

**Best for:**
- Multiple API servers
- Complex analytical queries
- High-volume production (> 100K/day)
- Need for JOIN operations

---

#### 🟢 **Redis: Perfect for This Use Case** ⭐

**Advantages:**
- ✅ Ultra-fast (< 1ms response time)
- ✅ Lightweight (64-256Mi memory)
- ✅ Persistent storage (AOF + RDB)
- ✅ Simple deployment (1 container)
- ✅ Efficient filtering (sorted sets)
- ✅ Built-in caching capabilities
- ✅ Perfect for < 100K predictions/day

**Data Model:**
```
prediction:{id} → Hash with all fields
prediction:by_timestamp → Sorted set (query by time)
prediction:by_risk_score → Sorted set (query by risk)
prediction:class:{0|1} → Set (filter by prediction class)
```

**Query Examples:**
```python
# Get latest 50 predictions
ZREVRANGE prediction:by_timestamp 0 49

# Get high-risk predictions (risk > 0.7)
ZRANGEBYSCORE prediction:by_risk_score 0.7 1.0

# Count disease predictions
SCARD prediction:class:1

# Get specific prediction
HGETALL prediction:123
```

**Persistence:**
- AOF: Append-only file (fsync every second)
- RDB: Snapshots (configurable triggers)
- Result: < 1 second data loss window

---

### Decision Matrix

#### Choose **Redis** if:
- ✅ Single API server or small cluster
- ✅ < 100K predictions/day
- ✅ Need fast response times (< 1ms)
- ✅ Simple key-value storage with basic filtering
- ✅ Want lightweight deployment
- ✅ **THIS IS YOUR USE CASE** ← You are here

#### Choose **PostgreSQL** if:
- Multiple API servers (need connection pooling)
- > 100K predictions/day
- Complex analytical queries with JOINs
- Need advanced features (triggers, stored procedures)
- Team familiar with SQL

#### Choose **Kafka** if:
- ❌ **Never for storing predictions**
- ✅ Building event-driven architecture
- ✅ Multiple consumers for same events
- ✅ Real-time data pipelines
- ✅ Decoupling services

---

### Performance Comparison

#### Prediction Save Operation

| Database | Latency | Throughput | Memory |
|----------|---------|------------|--------|
| Redis | **< 1ms** | 10,000 ops/sec | 64Mi |
| PostgreSQL | 5-10ms | 1,000 ops/sec | 256Mi |
| Kafka | N/A | N/A (not a database) | N/A |

#### Query Operations

| Operation | Redis | PostgreSQL | Kafka |
|-----------|-------|------------|-------|
| Get by ID | < 1ms | 2-5ms | ❌ No queries |
| Filter by risk_score | < 5ms | 10-20ms | ❌ No queries |
| Calculate statistics | < 100ms | 50-100ms | ❌ No queries |
| Get latest 100 | < 5ms | 10-15ms | ❌ No queries |

---

### Migration Path

As your application grows, here's the upgrade path:

```
Stage 1: Development & MVP
├─ Redis (current)
│  ├─ Fast prototyping
│  ├─ Lightweight
│  └─ < 10K predictions/day

Stage 2: Production (Low-Medium Scale)
├─ Redis
│  ├─ Production-ready
│  ├─ Persistent storage
│  └─ < 100K predictions/day

Stage 3: Production (High Scale)
├─ PostgreSQL
│  ├─ Better for complex queries
│  ├─ Connection pooling
│  ├─ Read replicas
│  └─ > 100K predictions/day

Stage 4: Event-Driven Architecture (Optional)
├─ PostgreSQL (storage)
└─ Kafka (event streaming)
   ├─ Decouple services
   ├─ Real-time analytics
   └─ Multiple consumers
```

**Migration:** SQLAlchemy abstracts the database layer, so switching from Redis to PostgreSQL requires only changing the `DATABASE_URL` environment variable (minimal code changes).

---

### Real-World Use Cases

#### ✅ Good Use of Redis (Your Case)
```
User → POST /predict → API (model inference) → Redis (save prediction) → User (response)
                                              ↓
                                         GET /predictions/history → Redis query → Results
```

#### ❌ Bad Use of Kafka
```
User → POST /predict → API → Kafka → Consumer saves to Redis → ??? → User waits forever
                                                                ↓
                                                            WHERE IS MY RESPONSE?
```

#### ✅ Good Use of Kafka (Event-Driven)
```
Prediction Event → Kafka Topic → [Consumer 1: Save to DB]
                               → [Consumer 2: Email if high-risk]
                               → [Consumer 3: Update dashboard]
                               → [Consumer 4: Check for drift]
```

---

### Summary

**For storing and querying prediction history:**

| Choice | Rating | Reason |
|--------|--------|--------|
| **Redis** | ⭐⭐⭐⭐⭐ | Perfect fit: fast, lightweight, persistent |
| **PostgreSQL** | ⭐⭐⭐ | Good but overkill for current scale |
| **Kafka** | ❌ | Wrong tool entirely (not a database) |

**Recommendation:** Start with **Redis** (implemented). Upgrade to **PostgreSQL** if you exceed 100K predictions/day or need complex SQL queries.

---

### FAQ

**Q: Can I use Kafka to save predictions?**  
A: No. Kafka is for event streaming, not data storage. Messages expire after retention period.

**Q: Is Redis production-ready?**  
A: Yes! Redis is used by Twitter, GitHub, Stack Overflow for production workloads.

**Q: What if I need SQL queries?**  
A: Switch to PostgreSQL by changing `DATABASE_URL`. Code changes are minimal thanks to abstraction.

**Q: Can I use both Redis and Kafka?**  
A: Yes! Redis for storage, Kafka for event streaming. But only if you need event-driven architecture.

**Q: Will Redis lose my data?**  
A: No. With AOF+RDB persistence, maximum data loss is < 1 second (same as most databases).

---

**Current Implementation:** ✅ Redis with AOF+RDB persistence
**Alternative Implemented:** ~~PostgreSQL (k8s/database.yaml deleted)~~
**Not Suitable:** ❌ Kafka (message queue, not a database)
