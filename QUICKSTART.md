# 🚀 Quick Start Guide
> Get your Heart Disease Prediction API running locally in minutes!

## 📋 Overview

Deploy the complete MLOps pipeline with **three options**:

| Option | Use Case | Time | Components |
|--------|----------|------|------------|
| 🔧 **Development** | Quick testing & iteration | 2 min | API only |
| 🐳 **Docker** | Isolated environment | 3 min | API + Monitoring |
| ☸️ **Kubernetes** | Production-like setup | 10 min | API + Redis + Monitoring + MLflow |

---

## ✅ Prerequisites

```powershell
# 1. Clone & Navigate
git clone <repository-url>
cd heart-disease-mlops

# 2. Create Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Prepare Data & Train Model (First time only)
python data/download_data.py
python scripts/train_model.py
```

**What happens:** Downloads Heart Disease UCI dataset → Trains Logistic Regression & Random Forest → Saves best model → Logs to MLflow

---

## 🔧 Option 1: Development Mode
**Best for:** Quick testing and model iteration

```powershell
# Start API
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Access Points
- **Swagger Docs:** http://localhost:8000/docs (Interactive API testing)
- **Health Check:** http://localhost:8000/health
- **ReDoc:** http://localhost:8000/redoc

### 🧪 Test Prediction
```powershell
# Run test script
python scripts/test_api.py

# Or use curl
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d "@test_data.json"
```

**Note:** Development mode doesn't include database or monitoring. Predictions are not stored.

---

## 🐳 Option 2: Docker
**Best for:** Isolated testing with monitoring stack

### Single Container
```powershell
# Build & Run
docker build -t heart-disease-api:latest .
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest

# Test
curl http://localhost:8000/health

# View logs
docker logs -f heart-api

# Stop & Remove
docker stop heart-api && docker rm heart-api
```

### Full Stack with Docker Compose
```powershell
# Start all services (API + Prometheus + Grafana)
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

### 🌐 Access Points
- **API:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

---

## ☸️ Option 3: Kubernetes (Production-Like)
**Best for:** Full MLOps experience with persistence and monitoring

### 🎯 What You'll Deploy
A complete MLOps stack with 8 pods running locally:
- **Heart Disease API** (1 pod) - ML prediction service
- **Redis** (1 pod) - Prediction history cache with persistence
- **MLflow** (1 pod) - Experiment tracking with Model Registry
- **Prometheus** (1 pod) - Metrics collection
- **Grafana** (1 pod) - Visualization dashboards
- **Loki** (1 pod) - Log aggregation
- **Promtail** (1 pod) - Log shipping
- **Redis Exporter** (1 pod) - Redis metrics exporter

### Prerequisites
- Rancher Desktop or Docker Desktop with Kubernetes enabled
- `kubectl` configured and pointing to local cluster
- PowerShell (for Windows deployment scripts)

### 🚀 Deploy
```powershell
# 1. Verify Kubernetes is ready
kubectl cluster-info
kubectl get nodes

# 2. Build image (local registry)
docker build -t heart-health-classifier:latest .

# 3. Deploy infrastructure (order matters!)
kubectl apply -f k8s/redis.yaml              # Redis cache
kubectl apply -f k8s/redis-exporter.yaml     # Redis metrics
kubectl apply -f k8s/monitoring-local.yaml   # Prometheus + Grafana
kubectl apply -f k8s/deployment.yaml         # Heart Disease API

# 4. Deploy MLflow (experiment tracking)
.\scripts\deploy-mlflow.ps1

# 5. Wait for all pods to be ready
kubectl get pods -w
# Press Ctrl+C when all pods show "Running"

# 6. Verify deployment
kubectl get all
kubectl get ingress  # Optional: View ingress placeholders
```

### 🌐 Access Points (NodePort)
All services are accessible via direct NodePort access:

- **API Swagger UI:** http://localhost:30080/docs
- **API Health Check:** http://localhost:30080/health
- **Grafana Dashboard:** http://localhost:30030 (login: admin/admin)
- **MLflow UI:** http://localhost:30050 (experiments & models)
- **Prometheus Metrics:** http://localhost:30090

**Note:** Ingress endpoints exist as placeholders but NodePort is the recommended access method for local development.

### 🧪 Test Complete Workflow
```powershell
# 1. Health check
curl http://localhost:30080/health

# 2. Make prediction (auto-saved to Redis)
Invoke-RestMethod -Uri "http://localhost:30080/predict" -Method Post `
  -ContentType "application/json" `
  -Body (@{
    age=63; sex=1; cp=3; trestbps=145; chol=233; fbs=1;
    restecg=0; thalach=150; exang=0; oldpeak=2.3;
    slope=0; ca=0; thal=1
  } | ConvertTo-Json)

# 3. View prediction history
Invoke-RestMethod -Uri "http://localhost:30080/predictions/history?limit=10"

# 4. View statistics
Invoke-RestMethod -Uri "http://localhost:30080/predictions/stats"

# 5. Check Redis metrics in Grafana
# Open: http://localhost:30030
# Navigate to: "Redis Prediction Cache" dashboard

# 6. View MLflow experiments
# Open: http://localhost:30050
# Explore training runs and model artifacts

# 7. Check Prometheus targets
# Open: http://localhost:30090/targets
# Verify all services are being scraped
```

### 📊 View Logs
```powershell
# API logs
kubectl logs -l app=heart-disease-api -f

# Redis logs
kubectl logs -l app=redis --tail=50

# All components
kubectl logs -l app --prefix=true -f
```

### 🔄 Update Deployment
```powershell
# Rebuild image
docker build -t heart-health-classifier:latest --no-cache .

# Restart deployment (picks up new image)
kubectl rollout restart deployment heart-disease-api

# Check rollout status
kubectl rollout status deployment heart-disease-api

# Restart all services
kubectl rollout restart deployment --all
```

### 🛑 Clean Up
```powershell
# Delete all deployments (keeps PVC/data for Redis and MLflow)
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/monitoring-local.yaml
kubectl delete -f k8s/mlflow.yaml
kubectl delete -f k8s/redis-exporter.yaml
kubectl delete -f k8s/redis.yaml
kubectl delete -f k8s/ingress.yaml  # If deployed

# Or delete everything including persistent data
kubectl delete all --all
kubectl delete pvc --all
```

---

## 📊 MLflow Experiment Tracking

### Option A: Kubernetes MLflow (Recommended)
If you deployed with Kubernetes (Option 3), MLflow is already running:

**Access MLflow UI:** http://localhost:30050

**Features:**
- View all training experiments
- Compare model runs (Logistic Regression vs Random Forest)
- Access model artifacts and parameters
- Model Registry with versioning
- Persistent storage via PersistentVolume

**Deploy MLflow separately** (if not done during setup):
```powershell
.\scripts\deploy-mlflow.ps1
```

### Option B: Local MLflow UI
For development mode (Option 1) or Docker (Option 2):

```powershell
# Start MLflow UI locally
python -m mlflow ui --port 5000
```

Visit http://localhost:5000 to view experiments from `mlruns_training/` directory.

---

## 🧪 Run Tests

```powershell
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov=api --cov-report=html

# Open coverage report
start htmlcov/index.html

# Test database integration (Kubernetes only)
python scripts/test_database.py
```

---

## 🐛 Troubleshooting

<details>
<summary><b>Model not found error</b></summary>

```powershell
# Train the model first
python scripts/train_model.py
```
</details>

<details>
<summary><b>Port 8000 already in use</b></summary>

```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn api.app:app --port 8001
```
</details>

<details>
<summary><b>Kubernetes pod not starting</b></summary>

```powershell
# Check pod status
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```
</details>

<details>
<summary><b>Docker image not found in Kubernetes</b></summary>

```powershell
# Rebuild with correct tag
docker build -t heart-health-classifier:latest .

# Check image exists
docker images | grep heart-health-classifier

# Verify deployment uses correct image
kubectl describe deployment heart-disease-api | Select-String -Pattern "Image:"

# Update deployment imagePullPolicy if needed
kubectl edit deployment heart-disease-api
# Set: imagePullPolicy: Never (for local images)
```
</details>

<details>
<summary><b>Redis connection failed</b></summary>

```powershell
# Check Redis is running
kubectl get pods -l app=redis

# Test connectivity from API pod
kubectl exec -it deployment/heart-disease-api -- sh
ping redis
telnet redis 6379

# Check Redis logs
kubectl logs -l app=redis --tail=50
```
</details>

<details>
<summary><b>MLflow UI not accessible</b></summary>

```powershell
# Check MLflow pod status
kubectl get pods -l app=mlflow

# Check MLflow logs
kubectl logs -l app=mlflow --tail=50

# Verify service is exposed
kubectl get svc mlflow-service

# Test connectivity
curl http://localhost:30050

# Redeploy MLflow if needed
.\scripts\deploy-mlflow.ps1
```
</details>

<details>
<summary><b>Grafana dashboards not loading</b></summary>

```powershell
# Check Grafana pod
kubectl get pods -l app=grafana

# Check Grafana logs
kubectl logs -l app=grafana --tail=50

# Verify Prometheus datasource
# In Grafana UI: Configuration → Data Sources
# Should see Prometheus at http://prometheus:9090

# Restart Grafana
kubectl rollout restart deployment grafana
```
</details>

---

## 🎯 What You've Built

✅ **ML Pipeline:** Data processing → Feature engineering → Model training  
✅ **REST API:** FastAPI with automatic validation and documentation  
✅ **Database:** Redis with persistence for prediction history  
✅ **Monitoring:** Prometheus + Grafana dashboards with custom panels  
✅ **Experiment Tracking:** MLflow with Model Registry and artifact storage  
✅ **Containerization:** Docker with multi-stage builds  
✅ **Orchestration:** Kubernetes with StatefulSets, PersistentVolumes, and NodePort services  
✅ **Testing:** Unit tests with 61% coverage reporting  
✅ **CI/CD Ready:** Infrastructure-as-code with declarative YAML manifests  

---

## 📚 Next Steps

- **Customize Models:** Modify `src/model_training.py` for different algorithms
- **Add Features:** Extend `src/feature_engineering.py` with domain knowledge
- **Scale:** Increase replicas in `k8s/deployment.yaml`
- **Secure:** Add authentication to API endpoints
- **Monitor:** Create custom Grafana dashboards

---

**🎓 Happy Building!**
