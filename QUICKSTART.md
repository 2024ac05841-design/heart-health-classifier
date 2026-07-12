# 🚀 Quick Start Guide
> Deploy a complete MLOps pipeline with Kubernetes in 10 minutes!

## 📋 Overview

Deploy a **production-ready** Heart Disease Prediction system with:

| Component | Description | Port |
|-----------|-------------|------|
| 🫀 **ML API** | FastAPI prediction service with automatic validation | 30080 |
| 💾 **Redis** | Prediction history cache with persistence | - |
| 📊 **MLflow** | Experiment tracking & Model Registry | 30050 |
| 📈 **Prometheus** | Metrics collection & monitoring | 30090 |
| 🎨 **Grafana** | Visualization dashboards | 30030 |
| 📝 **Loki + Promtail** | Centralized logging | - |

**Deployment Time:** ~10 minutes  
**Total Pods:** 8 running containers  
**Architecture:** Full MLOps stack with monitoring, logging, and persistence

---

## 📦 Prerequisites & Setup

### System Requirements
- **Kubernetes:** Rancher Desktop or Docker Desktop with K8s enabled
- **Tools:** `kubectl`, PowerShell (Windows), Python 3.11+
- **Resources:** 4GB RAM minimum, 10GB disk space

### Initial Setup
```powershell
# 1. Clone repository
git clone <repository-url>
cd heart-disease-mlops

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare data & train models
python data/download_data.py
python scripts/train_model.py
```

**What happens:** Downloads Heart Disease UCI dataset → Trains Logistic Regression & Random Forest → Saves best model → Logs experiments to MLflow

---

## ☸️ Kubernetes Deployment

### 🎯 What You'll Deploy

A complete **8-pod MLOps stack** running locally on Kubernetes:

| Pod | Role | Resources |
|-----|------|-----------|
| 🫀 **Heart Disease API** | ML prediction service with FastAPI | 256Mi RAM |
| 💾 **Redis** | Prediction history & caching | 256Mi RAM |
| 📊 **MLflow** | Experiment tracking & Model Registry | 3GB RAM |
| 📈 **Prometheus** | Metrics collection & alerting | 512Mi RAM |
| 🎨 **Grafana** | Dashboards & visualization | 512Mi RAM |
| 📝 **Loki** | Log aggregation | 610Mi RAM |
| 🔍 **Promtail** | Log shipping agent | 84Mi RAM |
| 📊 **Redis Exporter** | Redis metrics for Prometheus | 128Mi RAM |

**Total Resources:** ~5.3GB RAM

---

### 🚀 Deploy to Kubernetes
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

# 5. Register best model to MLflow Model Registry
python scripts/register_best_model.py

# 6. Wait for all pods to be ready
kubectl get pods -w
# Press Ctrl+C when all pods show "Running"

# 7. Verify deployment
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

# 6. View MLflow experiments and registered model
# Open: http://localhost:30050
# Experiments: View all training runs and artifacts
# Models: View registered model "heart-disease-predictor" in Production

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

### Access MLflow UI

**URL:** http://localhost:30050

### Features

| Feature | Description |
|---------|-------------|
| 🧪 **Experiments** | View all training runs with metrics and parameters |
| 🔀 **Compare Runs** | Side-by-side comparison of Logistic Regression vs Random Forest |
| 📦 **Artifacts** | Access model files, environment specs, and dependencies |
| 🏷️ **Model Registry** | Version control for ML models with stage management |
| 💾 **Persistence** | Data stored in PersistentVolume (survives pod restarts) |

### Model Registry

After deployment, the best model is registered automatically:

```powershell
# Deploy MLflow and upload experiments
.\scripts\deploy-mlflow.ps1

# Register best model to Model Registry
python scripts/register_best_model.py
```

**What happens:**
1. 🔗 Connects to MLflow at http://localhost:30050
2. 🏆 Registers **Random Forest** model (98.4% accuracy)
3. 📝 Creates Model Registry entry: `heart-disease-predictor`
4. 🏷️ Adds metadata (accuracy: 0.984, roc_auc: 1.0, model_type: RandomForest)
5. ⚡ Sets stage to **Production**
6. 🌐 Available at: http://localhost:30050/#/models/heart-disease-predictor

---

## 🧪 Testing

### Run Unit Tests

```powershell
# Run all tests with coverage
pytest tests/ -v --cov=src --cov=api --cov-report=html

# View coverage report in browser
start htmlcov/index.html

# Test Redis integration
python scripts/test_database.py
```

**Test Coverage:** 61% (src + api modules)  
**Test Suites:** 21 passing tests across 3 test files

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

<details>
<summary><b>Model registration failed</b></summary>

```powershell
# Ensure MLflow is running
kubectl get pods -l app=mlflow

# Verify MLflow is accessible
curl http://localhost:30050

# Check if experiments were uploaded
# Open: http://localhost:30050
# Look for experiment "heart_disease_prediction"

# Re-run model registration
python scripts/register_best_model.py

# Check registration logs for errors
# Common issues:
# - MLflow pod not ready (wait a few seconds)
# - Experiments not uploaded (run deploy-mlflow.ps1 first)
# - Run ID not found (verify run exists in MLflow UI)
```
</details>

---

## 🎯 What You've Built

A **production-ready MLOps system** with enterprise-grade capabilities:

### 🤖 Machine Learning
- **ML Pipeline:** Data processing → Feature engineering → Model training
- **Experiment Tracking:** MLflow with Model Registry and artifact storage  
- **Model Deployment:** Best performing model (98.4% accuracy) in production

### 🌐 API & Services
- **REST API:** FastAPI with automatic validation, documentation, and OpenAPI specs
- **Database:** Redis with persistence for prediction history
- **Monitoring:** Prometheus metrics collection with custom exporters

### 📊 Observability
- **Dashboards:** Grafana with pre-configured panels for API, Redis, and infrastructure metrics
- **Logging:** Centralized logging with Loki + Promtail
- **Alerting:** Prometheus-based alerting rules (ready for configuration)

### ⚙️ Infrastructure
- **Containerization:** Docker with multi-stage builds and optimized images
- **Orchestration:** Kubernetes with StatefulSets, PersistentVolumes, NodePort services
- **Testing:** Unit tests with 61% coverage  
- **CI/CD Ready:** Infrastructure-as-code with declarative YAML manifests

---

## 📚 Next Steps

### 🔧 Customize & Extend
- **Models:** Modify [src/model_training.py](src/model_training.py) for different ML algorithms
- **Features:** Extend [src/feature_engineering.py](src/feature_engineering.py) with domain knowledge
- **API:** Add new endpoints in [api/routers/](api/routers/)

### 📈 Scale & Optimize
- **Horizontal Scaling:** Increase replicas in [k8s/deployment.yaml](k8s/deployment.yaml)
- **Resource Limits:** Tune memory/CPU allocations per pod
- **Caching:** Optimize Redis TTL and eviction policies

### 🔒 Production Readiness
- **Authentication:** Add JWT/OAuth to API endpoints
- **Secrets Management:** Use Kubernetes Secrets for sensitive data
- **TLS/HTTPS:** Configure ingress with cert-manager
- **Monitoring:** Create custom Grafana dashboards and Prometheus alerts

---

**🎓 Happy Building! Need help? Check the troubleshooting section above or open an issue.**
