# 📂 Project Structure

## Complete File Tree

```
heart-disease-mlops/
│
├── 📄 README.md                          # Main documentation with diagrams
├── 📄 QUICKSTART.md                      # Quick start guide
├── 📄 PROJECT_REPORT.md                  # Comprehensive 10-page project report (NEW)
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies (full)
├── 📄 requirements-runtime.txt           # Runtime dependencies only (NEW)
├── 📄 environment.yml                    # Conda environment
├── 📄 pytest.ini                         # Pytest configuration
├── 📄 .coveragerc                        # Coverage configuration (NEW)
├── 📄 Dockerfile                         # Container definition
├── 📄 .dockerignore                      # Docker ignore file
├── 📄 docker-compose.yml                 # Multi-container setup
├── 📄 Makefile                           # Common commands
├── 📄 .gitignore                         # Git ignore file
├── 📄 mlflow.db                          # MLflow tracking database (NEW)
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 ci-cd.yml                  # GitHub Actions CI/CD pipeline
│
├── 📁 api/                               # API Implementation
│   ├── 📄 __init__.py
│   ├── 📄 app.py                         # FastAPI application with Redis integration
│   ├── 📄 database.py                    # Redis connection management
│   ├── 📄 db_models.py                   # Redis data models for predictions
│   ├── 📄 models.py                      # Pydantic request/response models
│   ├── 📄 dependencies.py                # Dependency injection
│   ├── 📄 constants.py                   # Application constants
│   ├── 📄 monitoring.py                  # Prometheus metrics
│   └── 📁 routers/                       # API route handlers
│       ├── 📄 __init__.py
│       ├── 📄 health.py                  # Health check endpoint
│       ├── 📄 predict.py                 # Prediction endpoint with Redis storage
│       ├── 📄 model_info.py              # Model information endpoint
│       ├── 📄 test_data.py               # Test data generation
│       └── 📄 history.py                 # Prediction history & statistics
│
├── 📁 data/                              # Data Management
│   ├── 📄 README.md                      # Data instructions
│   ├── 📄 download_data.py               # Dataset download script
│   ├── 📄 create_sample_data.py          # Sample data generator
│   └── 📁 raw/                           # Raw data storage
│       └── 📄 heart_disease.csv          # Dataset (303 samples)
│
├── 📁 k8s/                               # Kubernetes Configuration
│   ├── 📄 README.md                      # Kubernetes deployment guide
│   ├── 📄 deployment.yaml                # API deployment (generic)
│   ├── 📄 deployment-local.yaml          # Local deployment (Rancher Desktop) (NEW)
│   ├── 📄 deployment-cloud.yaml          # Cloud deployment configuration (NEW)
│   ├── 📄 redis.yaml                     # Redis StatefulSet + Services
│   ├── 📄 redis-exporter.yaml            # Redis metrics exporter
│   ├── 📄 mlflow.yaml                    # MLflow server deployment (NEW)
│   ├── 📄 monitoring-local.yaml          # Prometheus + Grafana + Loki stack (NEW)
│   ├── 📄 loki-stack.yaml                # Loki logging stack (NEW)
│   ├── 📄 configmap.yaml                 # Configuration map
│   └── 📄 ingress.yaml                   # Ingress controller config (NEW)
│
├── 📁 models/                            # Model Artifacts
│   ├── 📄 best_model.pkl                 # Trained model (Random Forest)
│   ├── 📄 scaler.pkl                     # StandardScaler
│   ├── 📄 feature_names.json             # Feature metadata
│   └── 📄 metrics.json                   # Model performance metrics
│
├── 📁 monitoring/                        # Monitoring Configuration
│   ├── 📄 README.md                      # Monitoring documentation
│   ├── 📄 prometheus.yml                 # Prometheus config (API + Redis metrics)
│   ├── 📄 alerts.yml                     # Alert rules
│   ├── 📄 MLFLOW.md                      # MLflow setup guide (NEW)
│   ├── 📄 MODEL_DEPLOYMENT.md            # Model deployment guide (NEW)
│   ├── 📄 grafana-dashboard.json         # ML monitoring dashboard
│   ├── 📄 grafana-home-dashboard.json    # Infrastructure overview dashboard
│   ├── 📄 grafana-advanced-dashboard.json # Advanced metrics dashboard
│   ├── 📄 grafana-logs-dashboard.json    # Logs & filtering dashboard
│   └── 📄 grafana-dashboard-predictions.json # Predictions history dashboard
│
├── 📁 project-docs/                      # Project Documentation
│   ├── 📄 PROJECT_STRUCTURE.md           # This file
│   ├── 📄 PROJECT_SUMMARY.md             # Project completion summary
│   ├── 📄 MODEL_CARD.md                  # Model documentation
│   ├── 📄 CONTRIBUTING.md                # Contribution guidelines
│   ├── 📄 CHANGELOG.md                   # Version history
│   ├── 📄 DATABASE.md                    # Database integration guide
│   ├── 📄 DATABASE_COMPARISON.md         # Database comparison (NEW)
│   ├── 📄 DATABASE_IMPLEMENTATION.md     # Database implementation details (NEW)
│   ├── 📄 verify_setup.py                # Setup verification script
│   ├── 📄 MLOps Assignment 01 2026.pdf   # Assignment requirements (NEW)
│   └── 📄 A01 FAQs.pdf                   # Assignment FAQs (NEW)
│
├── 📁 screenshots/                       # Project Screenshots (NEW)
│   ├── 📄 README.md                      # Screenshots status tracker
│   ├── 📁 mlflow/                        # MLflow screenshots (9 images)
│   │   ├── 📄 mlflow_experiments_list.png
│   │   ├── 📄 mlflow_run_details.png
│   │   ├── 📄 mlflow_model_registry.png
│   │   ├── 📄 mlflow_metrics_comparison-1.png (Accuracy)
│   │   ├── 📄 mlflow_metrics_comparison-2.png (Recall)
│   │   ├── 📄 mlflow_metrics_comparison-3.png (ROC-AUC)
│   │   ├── 📄 mlflow_metrics_comparison-4.png (F1-Score)
│   │   ├── 📄 mlflow_metrics_comparison-5.png (Precision)
│   │   └── 📄 mlflow_artifacts.png
│   ├── 📁 cicd/                          # CI/CD screenshots (6 images)
│   │   ├── 📄 github_actions_workflow.png
│   │   ├── 📄 github_actions_tests.png
│   │   ├── 📄 github_actions_coverage.png
│   │   ├── 📄 github_actions_docker_build.png
│   │   ├── 📄 github_actions_security_scan.png
│   │   └── 📄 codecov_dashboard.png
│   └── 📁 kubernetes/                    # Kubernetes screenshots (16 images)
│       ├── 📄 kubectl_get_pods.png
│       ├── 📄 kubectl_get_services.png
│       ├── 📄 kubectl_describe_pod.png
│       ├── 📄 api_swagger_ui.png
│       ├── 📄 api_health_check.png
│       ├── 📄 api_prediction_response_1.png
│       ├── 📄 api_prediction_response_2.png
│       ├── 📄 grafana_home.png
│       ├── 📄 grafana_dashboard_1.png
│       ├── 📄 grafana_dashboard_2.png
│       ├── 📄 grafana_dashboard_3.png
│       ├── 📄 grafana_dashboard_4.png
│       ├── 📄 grafana_dashboard_5.png
│       ├── 📄 grafana_dashboard_6.png
│       ├── 📄 prometheus_targets.png
│       └── 📄 redis_cache_metrics.png
│
├── 📁 scripts/                           # Utility Scripts
│   ├── 📄 train_model.py                 # Model training script
│   ├── 📄 test_api.py                    # API testing script
│   ├── 📄 test_database.py               # Redis integration tests
│   ├── 📄 register_best_model.py         # MLflow model registration (NEW)
│   ├── 📄 deploy_local_rancher.ps1       # Rancher Desktop deployment (NEW)
│   ├── 📄 deploy-mlflow.ps1              # MLflow deployment script (NEW)
│   ├── 📄 deploy-mlflow.sh               # MLflow deployment (Linux/macOS) (NEW)
│   ├── 📄 deploy-predictions-dashboard.ps1 # Dashboard deployment (NEW)
│   ├── 📄 deploy-predictions-dashboard.sh  # Dashboard deployment (Linux) (NEW)
│   ├── 📄 cleanup_rancher.ps1            # Cleanup script (NEW)
│   ├── 📄 extract-models.ps1             # Model extraction script (NEW)
│   ├── 📄 docker_commands.sh             # Docker helper commands
│   └── 📄 k8s_commands.sh                # Kubernetes commands
│
├── 📁 src/                               # Core ML Logic
│   ├── 📄 __init__.py
│   ├── 📄 data_processing.py             # Data preprocessing
│   │   ├── DataProcessor class
│   │   ├── Missing value handling
│   │   ├── Feature scaling
│   │   └── Train/test split
│   ├── 📄 feature_engineering.py         # Feature engineering
│   │   ├── FeatureEngineer class
│   │   ├── Feature creation
│   │   └── Pipeline building
│   ├── 📄 model_training.py              # Model training
│   │   ├── ModelTrainer class
│   │   ├── Model training
│   │   ├── Evaluation
│   │   ├── MLflow logging
│   │   └── Cross-validation
│   └── 📄 utils.py                       # Helper functions
│       ├── File operations
│       ├── Logging setup
│       └── Artifact management
│
├── 📁 tests/                             # Test Suite
│   ├── 📄 __init__.py
│   ├── 📄 test_data_processing.py        # Data processing tests
│   │   ├── Test data loading
│   │   ├── Test preprocessing
│   │   └── Test pipeline
│   ├── 📄 test_feature_engineering.py    # Feature engineering tests
│   ├── 📄 test_model_training.py         # Model training tests
│   │   ├── Test training
│   │   ├── Test evaluation
│   │   └── Test persistence
│   └── 📄 test_api.py                    # API tests
│       ├── Test endpoints
│       ├── Test validation
│       └── Test responses
│
├── 📁 mlruns/                            # MLflow Tracking Server (NEW)
│   └── Experiment data (runtime)
│       ├── Parameters
│       ├── Metrics
│       └── Artifacts
│
├── 📁 mlruns_training/                   # MLflow Training Runs
│   └── Experiment data (training phase)
│       ├── Parameters
│       ├── Metrics
│       └── Artifacts
│
├── 📁 htmlcov/                           # Coverage HTML Reports (generated)
│   └── Coverage visualization
│
└── 📁 venv/                              # Virtual Environment
    └── Python packages
```

## Directory Descriptions

### 📁 Root Level Files
- **README.md** - Complete project documentation with architecture diagrams
- **QUICKSTART.md** - Get started in 5 minutes
- **PROJECT_REPORT.md** - Comprehensive 10-page MLOps project report with screenshots
- **requirements.txt** - All Python dependencies (development + runtime)
- **requirements-runtime.txt** - Runtime-only dependencies for Docker
- **Dockerfile** - Production-ready container image
- **docker-compose.yml** - Complete stack (API + Prometheus + Grafana)
- **mlflow.db** - SQLite database for MLflow tracking server

### 📁 API Layer (`api/`)
FastAPI application serving the ML model:
- **Modular router architecture** for clean code organization
- **RESTful endpoints** with automatic OpenAPI documentation
- **Redis integration** for prediction storage and history
- **Pydantic models** for request/response validation
- **Prometheus metrics** for monitoring
- **Health checks** with liveness/readiness probes

**Key Components:**
- `app.py` - Main FastAPI application with startup/shutdown events
- `database.py` - Redis connection pool management
- `db_models.py` - PredictionRecord model with Redis operations
- `routers/` - Separated route handlers:
  - `predict.py` - Prediction endpoint with automatic Redis storage
  - `history.py` - Query prediction history and statistics
  - `health.py`, `model_info.py`, `test_data.py` - Supporting endpoints

### 📁 Data Layer (`data/`)
Data management and preprocessing:
- Dataset download utilities
- Raw data storage
- Data cleaning and transformation
- Sample data generation

### 📁 Project Documentation (`project-docs/`)
Comprehensive project documentation:
- **PROJECT_STRUCTURE.md** - This file (complete project structure)
- **PROJECT_SUMMARY.md** - Assignment completion checklist
- **MODEL_CARD.md** - Model documentation and performance
- **DATABASE.md** - Redis integration guide
- **DATABASE_COMPARISON.md** - Database technology comparison
- **DATABASE_IMPLEMENTATION.md** - Implementation details
- **CHANGELOG.md** - Version history and updates
- **CONTRIBUTING.md** - Contribution guidelines
- **verify_setup.py** - Automated setup verification
- **Assignment PDFs** - Course materials and FAQs

### 📁 Screenshots (`screenshots/`)
Project screenshots for documentation:
- **mlflow/** - 9 MLflow UI screenshots (experiments, runs, registry, metrics)
- **cicd/** - 6 CI/CD pipeline screenshots (workflow, tests, coverage, Docker, security)
- **kubernetes/** - 16 Kubernetes screenshots (pods, services, Grafana dashboards, API)
- **README.md** - Screenshot status tracker (31/31 complete)

### 📁 Database Layer (Redis)
Prediction storage and retrieval:
- **In-memory database** with AOF and RDB persistence
- **Request history** with timestamp-based indexing
- **Statistics aggregation** (counts, averages, distributions)
- **Filtering capabilities** (by class, risk score, time range)
- **Grafana visualization** via Redis Exporter metrics

**Key Structure:**
- `request:{id}` - Hash containing full prediction record
- `request:id:counter` - Auto-incrementing ID
- `request:by_timestamp` - Sorted set for chronological queries
- `request:by_risk_score` - Sorted set for risk-based queries
- `request:class:{0|1}` - Sets grouped by prediction outcome

### 📁 ML Core (`src/`)
Machine learning logic:
- **data_processing.py** - Data preprocessing pipeline
- **feature_engineering.py** - Feature creation and transformation
- **model_training.py** - Model training and evaluation
- **utils.py** - Shared utilities

### 📁 Deployment (`k8s/`)
Kubernetes orchestration:
- **Multiple deployment configurations:**
  - `deployment.yaml` - Generic deployment template
  - `deployment-local.yaml` - Rancher Desktop configuration
  - `deployment-cloud.yaml` - Cloud provider configuration
- **Complete monitoring stack:**
  - `monitoring-local.yaml` - Prometheus + Grafana + Loki
  - `redis-exporter.yaml` - Redis metrics exporter
  - `mlflow.yaml` - MLflow tracking server
  - `loki-stack.yaml` - Centralized logging
- **Redis StatefulSet** with persistence
- **ConfigMap** for application configuration
- **Ingress** for external access
- **Health and readiness probes**
- **Resource limits and requests**

### 📁 CI/CD (`.github/workflows/`)
Automated pipeline:
- Code linting (Flake8, Black)
- Unit testing (Pytest)
- Docker image building
- Security scanning (Trivy)
- Artifact management

### 📁 Testing (`tests/`)
Comprehensive test suite:
- Unit tests for all modules
- Integration tests for API
- Feature engineering tests
- 89.59% code coverage (79 tests)
- Automated in CI/CD

### 📁 Scripts (`scripts/`)
Utility scripts:
- **Training:** `train_model.py`, `register_best_model.py`
- **Testing:** `test_api.py`, `test_database.py`
- **Deployment:** 
  - `deploy_local_rancher.ps1` - Local Rancher Desktop deployment
  - `deploy-mlflow.ps1` / `.sh` - MLflow server deployment
  - `deploy-predictions-dashboard.ps1` / `.sh` - Grafana dashboard setup
  - `cleanup_rancher.ps1` - Cleanup script
  - `extract-models.ps1` - Model extraction utility
- **Helpers:** `docker_commands.sh`, `k8s_commands.sh`

### 📁 Monitoring (`monitoring/`)
Observability stack:
- **Prometheus configuration** with scrape targets
- **Grafana dashboards** (5 comprehensive dashboards):
  - ML Monitoring (model performance, predictions)
  - Infrastructure Overview (system health)
  - Advanced Metrics (preprocessing, drift detection)
  - Logs & Filtering (Loki integration)
  - Predictions History (historical analysis)
- **Alert rules** for anomaly detection
- **Documentation:** MLFLOW.md, MODEL_DEPLOYMENT.md
- **Metrics collection** for API and Redis

### 📁 Models (`models/`)
Trained model artifacts:
- Best model (Random Forest)
- Preprocessing scaler
- Feature metadata
- Performance metrics

## File Counts

- **Total Files:** 100+
- **Python Files:** 25+
- **Configuration Files:** 20+
- **Documentation Files:** 15+
- **Test Files:** 4
- **Scripts:** 13
- **Screenshots:** 31 (9 MLflow + 6 CI/CD + 16 Kubernetes)
- **Kubernetes Manifests:** 11
- **Grafana Dashboards:** 5
- **Monitoring Configs:** 3

## Key Features by Directory

### `api/` - Production API
✅ FastAPI application  
✅ Automatic API documentation  
✅ Input validation  
✅ Error handling  
✅ Prometheus metrics  

### `src/` - ML Pipeline
✅ Data preprocessing  
✅ Feature engineering  
✅ Model training  
✅ MLflow integration  
✅ Cross-validation  

### `tests/` - Quality Assurance
✅ Unit tests  
✅ Integration tests  
✅ Code coverage  
✅ Automated testing  

### `k8s/` - Orchestration
✅ Kubernetes deployment  
✅ Service exposure  
✅ Health checks  
✅ Resource management  

### `.github/` - Automation
✅ CI/CD pipeline  
✅ Automated testing  
✅ Docker builds  
✅ Security scanning  

## Usage Patterns

### Development
```
src/ → tests/ → scripts/train_model.py → models/
```

### API Development
```
api/app.py → tests/test_api.py → Docker → K8s
```

### Model Training
```
data/ → src/ → MLflow → models/
```

### Deployment
```
Dockerfile → docker-compose.yml → k8s/ → Production
```

## Next Steps

1. **Explore:** Start with README.md for comprehensive overview
2. **Setup:** Follow QUICKSTART.md for rapid deployment
3. **Verify:** Run `python project-docs/verify_setup.py` to check environment
4. **Train:** Execute `python scripts/train_model.py` for model training
5. **Deploy:** Use Docker or Kubernetes deployment scripts
6. **Review Report:** Read PROJECT_REPORT.md for complete project documentation
7. **Monitor:** Access Grafana dashboards at http://localhost:30030

---



