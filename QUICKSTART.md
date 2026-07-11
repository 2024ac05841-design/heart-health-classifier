# 🚀 Quick Start Guide
> Get your Heart Disease Prediction API running locally in minutes!

## 📋 Overview

Deploy the complete MLOps pipeline with **three options**:

| Option | Use Case | Time | Components |
|--------|----------|------|------------|
| 🔧 **Development** | Quick testing & iteration | 2 min | API only |
| 🐳 **Docker** | Isolated environment | 3 min | API + Monitoring |
| ☸️ **Kubernetes** | Production-like setup | 5 min | API + Redis + Monitoring |

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

### Prerequisites
- Rancher Desktop or Docker Desktop with Kubernetes enabled
- `kubectl` configured

### 🚀 Deploy
```powershell
# 1. Verify Kubernetes is ready
kubectl cluster-info
kubectl get nodes

# 2. Build image (local registry)
docker build -t heart-disease-api:v1-redis .

# 3. Deploy infrastructure (order matters!)
kubectl apply -f k8s/redis.yaml           # Database
kubectl apply -f k8s/redis-exporter.yaml  # Metrics exporter
kubectl apply -f k8s/deployment.yaml      # API

# 4. Wait for pods to be ready
kubectl get pods -w
# Press Ctrl+C when all pods show "Running" and "1/1" or "2/2"

# 5. Verify deployment
kubectl get all
```

### 🌐 Access Points
- **API:** http://localhost:30080/docs
- **Grafana:** http://localhost:30030 (admin/admin)
- **Prometheus:** http://localhost:30090

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
docker build -t heart-disease-api:v1-redis --no-cache .

# Restart deployment (picks up new image)
kubectl rollout restart deployment heart-disease-api

# Check rollout status
kubectl rollout status deployment heart-disease-api
```

### 🛑 Clean Up
```powershell
# Delete all deployments (keeps PVC/data)
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/redis-exporter.yaml
kubectl delete -f k8s/redis.yaml

# Or delete everything including data
kubectl delete all --all
kubectl delete pvc --all
```

---

## 📊 MLflow Experiments
Track all model training experiments:

```powershell
# Start MLflow UI
mlflow ui --port 5000
```

Visit http://localhost:5000 to view:
- All training runs with metrics
- Model parameters and artifacts
- Performance comparisons

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
# Rebuild with specific tag
docker build -t heart-disease-api:v1-redis .

# Check image exists
docker images | grep heart-disease

# Update deployment imagePullPolicy
kubectl edit deployment heart-disease-api
# Change: imagePullPolicy: IfNotPresent
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

---

## 🎯 What You've Built

✅ **ML Pipeline:** Data processing → Feature engineering → Model training  
✅ **REST API:** FastAPI with automatic validation and documentation  
✅ **Database:** Redis with persistence for prediction history  
✅ **Monitoring:** Prometheus + Grafana dashboards  
✅ **Containerization:** Docker with optimized images  
✅ **Orchestration:** Kubernetes with StatefulSets and Services  
✅ **Testing:** Unit tests with coverage reporting  
✅ **Experiment Tracking:** MLflow for model versioning  

---

## 📚 Next Steps

- **Customize Models:** Modify `src/model_training.py` for different algorithms
- **Add Features:** Extend `src/feature_engineering.py` with domain knowledge
- **Scale:** Increase replicas in `k8s/deployment.yaml`
- **Secure:** Add authentication to API endpoints
- **Monitor:** Create custom Grafana dashboards

---

**🎓 Happy Building!**
