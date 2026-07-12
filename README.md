# 🫀 Heart Disease Prediction MLOps Project

[![CI/CD Pipeline](https://github.com/2024ac05841-design/heart-disease-mlops/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/2024ac05841-design/heart-disease-mlops/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Model Development](#model-development)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Contributors](#contributors)

---

## 🎯 Project Overview

This project implements an **end-to-end Machine Learning Operations (MLOps)** solution for predicting heart disease risk based on patient health data. The solution demonstrates modern MLOps best practices including:

- ✅ Automated data processing and feature engineering
- ✅ Experiment tracking with MLflow
- ✅ Model versioning and reproducibility
- ✅ RESTful API for model serving (FastAPI)
- ✅ Containerization with Docker
- ✅ Orchestration with Kubernetes
- ✅ CI/CD automation with GitHub Actions
- ✅ Comprehensive monitoring and logging

**Dataset:** Heart Disease UCI Dataset from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)

**Problem Statement:** Build a binary classification model to predict the presence/absence of heart disease based on 13 clinical features.

---

## 🏗️ Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph "Source Control"
        A[GitHub Repository] --> B[Code Push]
    end
    
    subgraph "CI/CD Pipeline - GitHub Actions"
        B --> C[Lint & Test]
        C --> D[Data Processing]
        D --> E[Model Training]
        E --> F[MLflow Logging]
        F --> G[Build Docker Image]
        G --> H[Security Scan]
        H --> I[Push to GHCR]
    end
    
    subgraph "Container Registry"
        I --> J[ghcr.io/heart-health-classifier]
    end
    
    subgraph "Kubernetes Cluster - 8 Pod MLOps Stack"
        J --> K[Deployment]
        
        subgraph "Application Layer"
            K --> L[Heart Disease API Pod]
            L --> M[Trained Model + Scaler]
            L --> N[Redis Service]
        end
        
        subgraph "Data Layer"
            N --> O[Redis StatefulSet]
            O --> P[PVC: 1Gi Storage]
            O --> Q[Prediction Cache]
            O --> R[Request History]
        end
        
        subgraph "Experiment Tracking"
            S[MLflow Server Pod]
            S --> T[PVC: 3Gi Artifacts]
            S --> U[SQLite Backend]
        end
        
        subgraph "Monitoring & Logging Stack"
            V[Prometheus Pod]
            W[Grafana Pod]
            X[Loki Pod]
            Y[Promtail Pod]
            Z[Redis Exporter Pod]
            
            L --> V
            O --> Z
            Z --> V
            V --> W
            L --> Y
            Y --> X
            X --> W
        end
        
        subgraph "Services"
            AA[API Service: NodePort 30080]
            AB[MLflow Service: NodePort 30050]
            AC[Grafana Service: NodePort 30030]
            AD[Prometheus Service: NodePort 30090]
        end
        
        L --> AA
        S --> AB
        W --> AC
        V --> AD
    end
    
    subgraph "End Users"
        AE[REST API Clients] --> AA
        AA --> L
        AF[Data Scientists] --> AB
        AG[DevOps/SRE] --> AC
        AG --> AD
    end
    
    subgraph "Monitoring Dashboards"
        W --> AH[Infrastructure Overview]
        W --> AI[ML Monitoring]
        W --> AJ[Advanced Metrics]
        W --> AK[Logs & Filtering]
        W --> AL[Prediction History]
    end
    
    style A fill:#e1f5ff
    style E fill:#ff9800
    style J fill:#2196f3
    style L fill:#4caf50
    style O fill:#ff6b6b
    style S fill:#9c27b0
    style V fill:#ffa726
    style W fill:#ab47bc
    style X fill:#66bb6a
```

### ML Pipeline Workflow

```mermaid
flowchart LR
    A[Start] --> B[Load Data]
    B --> C[Handle Missing Values]
    C --> D[Encode Target Variable]
    D --> E[Split Train/Test]
    E --> F[Scale Features]
    F --> G[Train Logistic Regression]
    F --> H[Train Random Forest]
    G --> I[Evaluate Models]
    H --> I
    I --> J[Cross-Validation]
    J --> K[Log to MLflow]
    K --> L[Select Best Model]
    L --> M[Save Model Artifacts]
    M --> N[End]
    
    style A fill:#4caf50
    style N fill:#f44336
    style L fill:#ff9800
```

### API Request Flow

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Model
    participant Redis
    participant Prometheus
    
    User->>API: POST /predict
    API->>API: Validate Input
    API->>Model: Load Model & Scaler
    Model->>Model: Preprocess Data
    Model->>Model: Make Prediction
    Model->>API: Return Prediction
    API->>Redis: Save Prediction Record
    Redis->>API: Confirm Save (ID)
    API->>Prometheus: Log Metrics
    API->>User: JSON Response with Prediction
    
    Note over User,API: Query History
    User->>API: GET /predictions/history
    API->>Redis: Query Records
    Redis->>API: Return Records
    API->>User: JSON Response with History
    
    Note over User,API: Health Check
    User->>API: GET /health
    API->>User: Status Response
```

### Deployment Architecture

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Namespace: production"
            A[ConfigMap] --> B[Deployment: API]
            B --> C[Pod 1: API]
            B --> D[Pod 2: API]
            C --> E[Service: LoadBalancer]
            D --> E
            
            R1[Redis ConfigMap] --> R2[Deployment: Redis]
            R2 --> R3[Pod: Redis]
            R3 --> R4[Service: Redis]
            R3 --> R5[PVC: Redis Data]
            
            C --> R4
            D --> R4
            
            RE1[Deployment: Redis Exporter] --> RE2[Pod: Exporter]
            RE2 --> R4
        end
        
        subgraph "Monitoring Stack"
            F[Prometheus]
            G[Grafana]
        end
        
        E --> F
        RE2 --> F
        F --> G
    end
    
    H[Internet] --> I[Load Balancer]
    I --> E
    
    style C fill:#42a5f5
    style D fill:#42a5f5
    style R3 fill:#ff6b6b
    style E fill:#66bb6a
    style F fill:#ffa726
    style G fill:#ab47bc
```

---

## ✨ Features

### 1. **Data Acquisition & EDA**
- Automated dataset download from UCI repository
- Comprehensive exploratory data analysis
- Professional visualizations (histograms, correlation heatmaps, class distribution)
- Missing value analysis and handling

### 2. **Feature Engineering & Model Development**
- Robust preprocessing pipeline (scaling, encoding)
- Multiple classification models (Logistic Regression, Random Forest)
- Hyperparameter tuning with GridSearchCV
- Cross-validation for model evaluation
- Comprehensive metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC

### 3. **Experiment Tracking**
- MLflow integration for experiment management
- Parameter, metric, and artifact logging
- Model versioning and comparison
- Visualization of training runs

### 4. **Model Packaging & Reproducibility**
- Model serialization (Joblib/Pickle)
- Preprocessing pipeline persistence
- Clean requirements.txt for dependency management
- Feature name tracking for inference

### 5. **CI/CD Pipeline**
- Automated linting (Flake8, Black)
- Unit tests with Pytest
- Code coverage reporting
- Automated Docker builds
- GitHub Actions workflow

### 6. **Model Containerization**
- Production-ready Dockerfile
- FastAPI-based REST API
- `/predict` endpoint with JSON I/O
- Health check and monitoring endpoints

### 7. **Production Deployment**
- Kubernetes deployment manifests
- Service exposure via LoadBalancer
- ConfigMap for environment variables
- Rolling updates and health checks

### 8. **Monitoring & Logging**
- Prometheus metrics integration
- **Redis metrics via Redis Exporter**
- **Grafana dashboards** (API metrics + Redis cache monitoring)
- API request logging
- Performance monitoring
- **Prediction history tracking**

### 9. **Documentation**
- Comprehensive README with diagrams
- Setup and installation instructions
- Architecture documentation
- API usage examples

---

## 🛠️ Technology Stack

| Category | Tools |
|----------|-------|
| **Programming** | Python 3.11+ |
| **ML Frameworks** | Scikit-learn, XGBoost |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Experiment Tracking** | MLflow |
| **API Framework** | FastAPI, Uvicorn |
| **Database** | Redis (in-memory with persistence) |
| **Testing** | Pytest, Pytest-cov |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes (Minikube/Cloud) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana, Redis Exporter |
| **Code Quality** | Flake8, Black, Pylint |

---

## 📁 Project Structure

```
heart-disease-mlops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # GitHub Actions CI/CD pipeline with model training
├── api/
│   ├── __init__.py
│   ├── app.py                     # FastAPI application with Redis integration
│   ├── database.py                # Redis connection management (NEW)
│   ├── db_models.py               # Redis data models (NEW)
│   ├── models.py                  # Pydantic request/response models
│   ├── dependencies.py            # Dependency injection
│   ├── constants.py               # Application constants
│   ├── monitoring.py              # Prometheus metrics
│   └── routers/                   # Modular route handlers
│       ├── __init__.py
│       ├── health.py              # Health check
│       ├── predict.py             # Prediction with Redis storage
│       ├── model_info.py          # Model information
│       ├── test_data.py           # Test data generation
│       └── history.py             # Prediction history queries (NEW)
├── data/
│   ├── raw/                       # Raw dataset storage
│   ├── create_sample_data.py      # Sample data generator
│   ├── download_data.py           # Dataset download script
│   ├── DATABASE.md                # Database integration guide (NEW)
│   └── README.md                  # Data documentation
├── k8s/
│   ├── deployment-local.yaml      # Kubernetes deployment (local - NodePort)
│   ├── deployment-cloud.yaml      # Kubernetes deployment (cloud - LoadBalancer)
│   ├── deployment.yaml            # Generic deployment (backward compatibility)
│   ├── redis.yaml                 # Redis deployment with persistence (NEW)
│   ├── redis-exporter.yaml        # Redis metrics exporter (NEW)
│   ├── configmap.yaml             # Configuration
│   └── README.md                  # Kubernetes deployment guide
├── models/
│   ├── feature_names.json         # Feature metadata (committed)
│   ├── metrics.json               # Model metrics (committed)
│   ├── best_model.pkl             # Trained model (built in CI/CD, not in git)
│   └── scaler.pkl                 # Feature scaler (built in CI/CD, not in git)
├── monitoring/
│   ├── prometheus.yml             # Prometheus configuration (API + Redis metrics)
│   ├── alerts.yml                 # Alert rules
│   ├── grafana-dashboard-predictions.json # Predictions history dashboard (NEW)
│   ├── grafana-home-dashboard.json # Infrastructure overview dashboard
│   ├── grafana-advanced-dashboard.json # Advanced metrics dashboard
│   ├── grafana-logs-dashboard.json # Logs & filtering dashboard
│   ├── grafana-dashboard.json     # ML monitoring dashboard
│   └── README.md                  # Monitoring documentation
├── project-docs/
│   ├── CHANGELOG.md               # Version history
│   ├── COMPLETION_REPORT.md       # Assignment completion report
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   ├── DATABASE_COMPARISON.md     # Database technology comparison (NEW)
│   ├── DATABASE_IMPLEMENTATION.md # Redis implementation details (NEW)
│   ├── MODEL_CARD.md              # Model documentation
│   ├── PROJECT_STRUCTURE.md       # Detailed structure
│   └── PROJECT_SUMMARY.md         # Project summary
├── scripts/
│   ├── train_model.py             # Main training script
│   ├── test_api.py                # API testing script
│   ├── test_database.py           # Redis integration tests (NEW)
│   ├── docker_commands.sh         # Docker helper commands
│   └── k8s_commands.sh            # Kubernetes helper commands
├── src/
│   ├── __init__.py
│   ├── data_processing.py         # Data preprocessing
│   ├── feature_engineering.py     # Feature engineering
│   ├── model_training.py          # Model training utilities
│   └── utils.py                   # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py    # Data processing tests
│   ├── test_model_training.py     # Model training tests
│   └── test_api.py                # API tests
├── .dockerignore                   # Docker ignore rules
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Multi-container setup with monitoring
├── environment.yml                 # Conda environment specification
├── LICENSE                         # MIT License
├── Makefile                        # Common commands
├── pytest.ini                      # Pytest configuration
├── QUICKSTART.md                   # Quick start guide
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── test_data.json                  # Sample test data for API
```

**Key Notes:**
- Model files (`*.pkl`) are trained during CI/CD pipeline and packaged in Docker images
- Models are **not** committed to git (reproducible builds from source)
- Docker images with trained models available at `ghcr.io/2024ac05841-design/heart-health-classifier`

**Generated Directories (not in git):**
- `mlruns_training/` - MLflow experiment tracking data (generated during local training)
- `.pytest_cache/` - Pytest cache directory
- `htmlcov/` - HTML coverage reports
- `.coverage`, `coverage.xml` - Test coverage files
- `venv/` - Python virtual environment
- `.vscode/` - VS Code settings (user-specific)

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Docker Desktop (for containerization)
- Kubernetes (Minikube or cloud provider)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/2024ac05841-design/heart-disease-mlops.git
cd heart-disease-mlops
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download Dataset

```bash
python data/download_data.py
```

This will download the Heart Disease UCI dataset to `data/raw/heart_disease.csv`.

### Step 5: Run Tests (Optional)

```bash
pytest tests/ -v
```

---

## 📊 Usage Guide

### 1. Train Models

```bash
python scripts/train_model.py --data-path data/raw/heart_disease.csv --output-dir models
```

**Arguments:**
- `--data-path`: Path to the dataset (default: `data/raw/heart_disease.csv`)
- `--output-dir`: Directory to save models (default: `models`)
- `--experiment-name`: MLflow experiment name (default: `heart_disease_prediction`)
- `--test-size`: Test set size (default: 0.2)

### 2. View MLflow Experiments

```bash
mlflow ui --port 5000
```

Visit `http://localhost:5000` to view experiment tracking.

### 3. Run API Locally

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 4. Test API

```bash
python scripts/test_api.py
```

Or use curl:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
    "thal": 1
  }'
```

---

## 🧪 Model Development

### Data Preprocessing

1. **Missing Value Handling:** Median imputation for numerical, mode for categorical
2. **Target Encoding:** Binary classification (0: No disease, 1: Disease present)
3. **Feature Scaling:** StandardScaler for normalization
4. **Train/Test Split:** 80/20 split with stratification

### Models Trained

#### 1. Logistic Regression
- Linear model for binary classification
- L2 regularization
- Max iterations: 1000

#### 2. Random Forest
- Ensemble of decision trees
- Number of estimators: 100
- Default hyperparameters with tuning

### Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **Accuracy** | Overall correctness |
| **Precision** | True positive rate |
| **Recall** | Sensitivity |
| **F1-Score** | Harmonic mean of precision and recall |
| **ROC-AUC** | Area under ROC curve |

### Cross-Validation

- 5-fold stratified cross-validation
- Ensures model generalization
- Reported with mean ± std deviation

---

## 📡 API Documentation

### Endpoints

#### **GET /**
Root endpoint with API information.

**Response:**
```json
{
  "message": "Heart Disease Prediction API",
  "version": "1.0.0",
  "status": "running"
}
```

#### **GET /health**
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "ml_model_loaded": true,
  "version": "1.0.0"
}
```

#### **POST /predict**
Predict heart disease risk.

**Request Body:**
```json
{
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
  "thal": 1
}
```

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Disease Present",
  "confidence": 0.85,
  "risk_score": 0.85
}
```

**Note:** All predictions are automatically saved to Redis for history tracking and analytics.

#### **GET /predictions/history** (NEW)
Query prediction history with filtering options.

**Query Parameters:**
- `limit` (default: 100, max: 1000) - Number of records to return
- `skip` (default: 0) - Records to skip for pagination
- `prediction_class` (optional: 0 or 1) - Filter by prediction outcome
- `min_risk_score` (optional: 0.0-1.0) - Minimum risk score filter
- `max_risk_score` (optional: 0.0-1.0) - Maximum risk score filter

**Example Request:**
```bash
curl "http://localhost:8000/predictions/history?limit=10&prediction_class=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "timestamp": "2026-07-11T10:30:00.123456",
    "patient_data": {...},
    "prediction": 1,
    "prediction_label": "Disease Present",
    "confidence": 0.85,
    "risk_score": 0.85,
    "inference_time_ms": 12.5,
    "preprocessing_time_ms": 3.2
  }
]
```

#### **GET /predictions/stats** (NEW)
Get aggregated statistics for all predictions.

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

#### **GET /predictions/{id}** (NEW)
Get a specific prediction by ID.

**Example Request:**
```bash
curl "http://localhost:8000/predictions/1"
```

**Response:**
```json
{
  "id": 1,
  "timestamp": "2026-07-11T10:30:00.123456",
  "patient_data": {...},
  "prediction": 1,
  "prediction_label": "Disease Present",
  "confidence": 0.85,
  "risk_score": 0.85
}
```

#### **GET /model/info**
Get model information.

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "features": ["age", "sex", "cp", ...],
  "n_features": 13,
  "scaler_loaded": true
}
```

#### **GET /metrics**
Prometheus metrics endpoint for monitoring.

---

## 🐳 Deployment

### Docker Deployment

#### Build Image

```bash
docker build -t heart-disease-api:latest .
```

#### Run Container

```bash
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest
```

#### Check Logs

```bash
docker logs heart-api
```

#### Stop Container

```bash
docker stop heart-api
docker rm heart-api
```

### Docker Compose (with Monitoring)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services:
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

### Kubernetes Deployment

We provide separate Kubernetes configurations for local testing and cloud production deployments:

- **`k8s/deployment-local.yaml`** - For Rancher Desktop, Minikube, Docker Desktop (NodePort service on port 30080)
- **`k8s/deployment-cloud.yaml`** - For AWS EKS, Azure AKS, Google GKE (LoadBalancer service)
- **`k8s/deployment.yaml`** - Generic deployment (backward compatibility)

See [`k8s/README.md`](k8s/README.md) for comprehensive deployment guide.

#### Using Rancher Desktop / Minikube (Local)

```bash
# Ensure kubectl is connected to local cluster
kubectl config use-context rancher-desktop  # or 'minikube' for Minikube

# Verify cluster
kubectl cluster-info

# Deploy Redis database first
kubectl apply -f k8s/redis.yaml

# Deploy Redis Exporter for metrics
kubectl apply -f k8s/redis-exporter.yaml

# Deploy application (uses ghcr.io image with trained model)
kubectl apply -f k8s/deployment-local.yaml

# Check deployment status
kubectl get pods
kubectl get services

# Verify Redis is running
kubectl get pods -l app=redis

# Access API (NodePort 30080)
curl http://localhost:30080/health

# Test prediction with Redis storage
curl -X POST "http://localhost:30080/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'

# Query prediction history
curl "http://localhost:30080/predictions/history?limit=10"

# View API documentation
# Open browser: http://localhost:30080/docs

# View Grafana dashboard (Redis metrics)
# Open browser: http://localhost:30030 (admin/admin)

# View logs
kubectl logs -l app=heart-disease-api

# Delete deployment
kubectl delete -f k8s/deployment-local.yaml
kubectl delete -f k8s/redis-exporter.yaml
kubectl delete -f k8s/redis.yaml
```

#### Using Cloud Kubernetes (GKE/EKS/AKS)

```bash
# Connect to your cloud cluster
# AWS: aws eks update-kubeconfig --name your-cluster
# Azure: az aks get-credentials --resource-group your-rg --name your-cluster
# GCP: gcloud container clusters get-credentials your-cluster --zone your-zone

# Deploy application (uses ghcr.io image)
kubectl apply -f k8s/deployment-cloud.yaml

# Check deployment
kubectl get pods
kubectl get services

# Wait for LoadBalancer external IP (may take 1-2 minutes)
kubectl get service heart-disease-api-service -w

# Once EXTERNAL-IP is assigned:
curl http://<EXTERNAL-IP>/health

# View logs
kubectl logs -l app=heart-disease-api

# Delete deployment
kubectl delete -f k8s/deployment-cloud.yaml
```

**Note:** The Docker image is automatically pulled from GitHub Container Registry and includes the trained model (no manual model upload needed).

---

## 📈 Monitoring

### Prometheus Metrics

The API exposes Prometheus metrics at `/metrics`:

- HTTP request count
- Request duration
- Request size
- Response size
- Active requests

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (when using docker-compose):

- **Credentials:** admin/admin
- **Pre-configured dashboards:** FastAPI metrics
- **Custom dashboards:** Create your own visualizations

### Application Logging

Logs are written to:
- Console (stdout)
- File: `logs/app.log`

Log format includes:
- Timestamp
- Log level
- Module name
- Message

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically:

1. **Linting:** Checks code quality with Flake8 and Black
2. **Testing:** Runs unit tests with Pytest and generates coverage reports
3. **Model Training:** Downloads data and trains the model from scratch
4. **Build:** Creates Docker image with trained model artifacts
5. **Container Registry:** Pushes image to GitHub Container Registry (ghcr.io)
6. **Security:** Scans for vulnerabilities with Trivy
7. **Artifacts:** Saves Docker image as downloadable artifact

### Trigger Events

- Push to `main` or `develop` branches (excluding documentation-only changes)
- Pull requests to `main`

**Note:** Pipeline skips execution for changes only to `*.md`, `project-docs/`, `LICENSE`, or `.gitignore`

### Pipeline Stages

```mermaid
graph TB
    A[Code Push] --> B{Doc Only?}
    B -->|Yes| Z[Skip Pipeline]
    B -->|No| C[Lint Code]
    C --> D[Run Tests]
    D --> E[Train Model]
    E --> F[Verify Model Files]
    F --> G[Build Docker Image]
    G --> H[Test Container]
    H --> I[Save Image Artifact]
    I --> J[Security Scan]
    J --> K[Push to ghcr.io]
    K --> L[Deployment Ready]
    
    style A fill:#4caf50
    style E fill:#ff9800
    style J fill:#f44336
    style K fill:#2196f3
    style Z fill:#9e9e9e
```

### Container Registry

Docker images are automatically published to:
- **Registry:** `ghcr.io/2024ac05841-design/heart-health-classifier`
- **Tags:** `latest` and `<commit-sha>`

Pull the latest image:
```bash
docker pull ghcr.io/2024ac05841-design/heart-health-classifier:latest
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_api.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov=api --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Test Categories

- **Unit Tests:** Test individual functions and classes
- **Integration Tests:** Test API endpoints
- **Data Tests:** Validate data processing

---

## 📝 Contributors

- **Your Name** - Initial work

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the dataset
- FastAPI documentation and community
- MLOps best practices from industry leaders

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: your.email@example.com

---

## 🎓 Assignment Details

**Course:** Machine Learning Operations (MLOps) AIMLCZG523  
**Assignment:** 01  
**Institution:** BITS Pilani


**Built with ❤️ for MLOps excellence**
