# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment

```powershell
# Clone repository (if not already done)
git clone https://github.com/yourusername/heart-disease-mlops.git
cd heart-disease-mlops

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Data & Train Model

```powershell
# Download dataset
python data/download_data.py

# Train models
python scripts/train_model.py
```

This will:
- Download the Heart Disease UCI dataset
- Preprocess the data
- Train Logistic Regression and Random Forest models
- Save the best model to `models/`
- Log experiments to MLflow

### 3. Run API Locally

```powershell
# Start the API
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Open your browser:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### 4. Test Prediction

Open a new terminal and run:

```powershell
python scripts/test_api.py
```

Or use the interactive API docs at http://localhost:8000/docs

---

## 🐳 Docker Quick Start

### Run with Docker

```powershell
# Build image
docker build -t heart-disease-api:latest .

# Run container
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest

# Test API
curl http://localhost:8000/health

# View logs
docker logs heart-api

# Stop container
docker stop heart-api
```

### Run with Docker Compose (includes monitoring)

```powershell
# Start all services
docker-compose up -d

# Access services
# API: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)

# Stop services
docker-compose down
```

---

## ☸️ Kubernetes Quick Start

### Minikube (Local)

```powershell
# Start Minikube
minikube start

# Build image in Minikube context
minikube docker-env | Invoke-Expression
docker build -t heart-disease-api:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Get service URL
minikube service heart-disease-api-service --url

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -l app=heart-disease-api -f
```

---

## 🧪 Testing

```powershell
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov=api --cov-report=html

# View coverage report
start htmlcov/index.html
```

---

## 📊 View Experiments

```powershell
# Start MLflow UI
mlflow ui --port 5000
```

Visit http://localhost:5000 to view all experiments, metrics, and models.

---

## 🔧 Common Commands

### Data Operations
```powershell
# Download fresh data
python data/download_data.py

# Explore data using Python
python -c "from src.data_processing import load_and_clean_data; df = load_and_clean_data('data/raw/heart_disease.csv'); print(df.describe())"
```

### Model Operations
```powershell
# Train with custom parameters
python scripts/train_model.py --test-size 0.3 --output-dir models/v2

# View model info
python -c "import joblib; model = joblib.load('models/best_model.pkl'); print(type(model).__name__)"
```

### API Operations
```powershell
# Run API in development mode
uvicorn api.app:app --reload

# Run API in production mode
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4

# Test specific endpoint
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d @test_data.json
```

### Docker Operations
```powershell
# Build image
docker build -t heart-disease-api:v1.0 .

# Run with volume mount (for development)
docker run -p 8000:8000 -v ${PWD}/models:/app/models heart-disease-api:latest

# Execute command in running container
docker exec -it heart-api bash

# Remove all containers and images
docker stop heart-api
docker rm heart-api
docker rmi heart-disease-api:latest
```

### Kubernetes Operations
```powershell
# Scale deployment
kubectl scale deployment heart-disease-api --replicas=3

# Update deployment
kubectl set image deployment/heart-disease-api api=heart-disease-api:v2.0

# Port forward for testing
kubectl port-forward service/heart-disease-api-service 8000:80

# Delete all resources
kubectl delete -f k8s/
```

---

## 🐛 Troubleshooting

### Issue: Model not found
**Solution:** Ensure you've trained the model first:
```powershell
python scripts/train_model.py
```

### Issue: Port 8000 already in use
**Solution:** Change the port or kill the process:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
uvicorn api.app:app --port 8001
```

### Issue: Docker build fails
**Solution:** Ensure Docker is running and you have sufficient disk space:
```powershell
docker system prune -a
```

### Issue: Kubernetes pod not starting
**Solution:** Check pod logs:
```powershell
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Issue: MLflow UI not showing experiments
**Solution:** Check if mlruns_training directory exists:
```powershell
# Create mlruns_training directory if missing
New-Item -ItemType Directory -Force -Path mlruns_training
```

---

## 📚 Next Steps

1. **Explore the Code:** Check out `src/` modules for data processing and model training
2. **Customize Models:** Modify hyperparameters in `src/model_training.py`
3. **Add Features:** Extend feature engineering in `src/feature_engineering.py`
4. **Deploy to Cloud:** Follow cloud-specific deployment guides in README.md
5. **Set up CI/CD:** Configure GitHub Actions with your repository

---

## 🎯 Learning Objectives Achieved

✅ Data preprocessing and feature engineering  
✅ Model training and evaluation  
✅ Experiment tracking with MLflow  
✅ API development with FastAPI  
✅ Containerization with Docker  
✅ Orchestration with Kubernetes  
✅ CI/CD pipeline setup  
✅ Monitoring and logging  
✅ Complete MLOps workflow  

---

**Happy Learning! 🎓**
