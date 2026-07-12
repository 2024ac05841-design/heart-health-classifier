# 📂 Project Structure

## Complete File Tree

```
heart-disease-mlops/
│
├── 📄 README.md                          # Main documentation with diagrams
├── 📄 QUICKSTART.md                      # Quick start guide
├── 📄 PROJECT_SUMMARY.md                 # Project completion summary
├── 📄 MODEL_CARD.md                      # Model documentation
├── 📄 CONTRIBUTING.md                    # Contribution guidelines
├── 📄 CHANGELOG.md                       # Version history
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies
├── 📄 environment.yml                    # Conda environment
├── 📄 pytest.ini                         # Pytest configuration
├── 📄 Dockerfile                         # Container definition
├── 📄 .dockerignore                      # Docker ignore file
├── 📄 docker-compose.yml                 # Multi-container setup
├── 📄 Makefile                           # Common commands
├── 📄 test_data.json                     # Sample test data
├── 📄 verify_setup.py                    # Setup verification script
├── 📄 .gitignore                         # Git ignore file
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
│       └── 📄 history.py                 # Prediction history & statistics (NEW)
│
├── 📁 data/                              # Data Management
│   ├── 📄 README.md                      # Data instructions
│   ├── 📄 DATABASE.md                    # Database integration guide (NEW)
│   ├── 📄 download_data.py               # Dataset download script
│   ├── 📄 create_sample_data.py          # Sample data generator
│   ├── 📁 raw/                           # Raw data storage
│   │   └── 📄 heart_disease.csv          # Dataset (303 samples)
│   └── 📁 processed/                     # Processed data (created at runtime)
│
├── 📁 k8s/                               # Kubernetes Configuration
│   ├── 📄 deployment.yaml                # API deployment with Redis env vars
│   │   ├── 2 replicas
│   │   ├── Health probes
│   │   ├── Resource limits
│   │   └── Redis connection config
│   ├── 📄 redis.yaml                     # Redis deployment & services (NEW)
│   │   ├── StatefulSet with persistence
│   │   ├── ConfigMap for Redis config
│   │   ├── PersistentVolumeClaim (2GB)
│   │   └── Services (ClusterIP + NodePort)
│   ├── 📄 redis-exporter.yaml            # Redis metrics exporter (NEW)
│   ├── � monitoring/                    # Monitoring dashboards (NEW)
│   │   └── 📄 grafana-dashboard-predictions.json  # Predictions dashboard
│   ├── 📄 configmap.yaml                 # Configuration map
│   └── Service (LoadBalancer)
│
├── 📁 models/                            # Model Artifacts
│   ├── 📄 best_model.pkl                 # Trained model (Random Forest)
│   ├── 📄 scaler.pkl                     # StandardScaler
│   ├── 📄 feature_names.json             # Feature metadata
│   └── 📄 metrics.json                   # Model performance metrics
│
├── 📁 monitoring/                        # Monitoring Configuration
│   ├── 📄 prometheus.yml                 # Prometheus config (API + Redis metrics)
│   └── 📁 grafana-dashboards/            # Grafana dashboards
│
├── 📁 scripts/                           # Training and utility scripts
│   ├── 📄 train_model.py                 # Main training script
│   ├── 📄 test_api.py                    # API testing script
│   ├── 📄 test_database.py               # Redis integration tests (NEW)
│   ├── 📄 docker_commands.sh             # Docker helper commands
│   └── 📄 k8s_commands.sh                # Kubernetes helper commands
│
├── 📁 scripts/                           # Utility Scripts
│   ├── 📄 train_model.py                 # Model training script
│   ├── 📄 test_api.py                    # API testing script
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
│   ├── 📄 test_model_training.py         # Model training tests
│   │   ├── Test training
│   │   ├── Test evaluation
│   │   └── Test persistence
│   └── 📄 test_api.py                    # API tests
│       ├── Test endpoints
│       ├── Test validation
│       └── Test responses
│
├── 📁 logs/                              # Application Logs (created at runtime)
│   └── 📄 app.log
│
├── 📁 mlruns_training/                   # MLflow Tracking (created at runtime)
│   └── Experiment data
│       ├── Parameters
│       ├── Metrics
│       └── Artifacts
│
└── 📁 venv/                              # Virtual Environment
    └── Python packages
```

## Directory Descriptions

### 📁 Root Level Files
- **README.md** - Complete project documentation with architecture diagrams
- **QUICKSTART.md** - Get started in 5 minutes
- **PROJECT_SUMMARY.md** - Assignment completion status
- **requirements.txt** - All Python dependencies
- **Dockerfile** - Production-ready container image
- **docker-compose.yml** - Complete stack (API + Prometheus + Grafana)

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
- **Database integration documentation** (DATABASE.md)

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
- Deployment with 2 replicas
- Service with LoadBalancer
- ConfigMap for configuration
- Health and readiness probes
- Resource limits

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
- >80% code coverage
- Automated in CI/CD

### 📁 Scripts (`scripts/`)
Utility scripts:
- Training automation
- API testing
- Docker helpers
- Kubernetes commands

### 📁 Monitoring (`monitoring/`)
Observability stack:
- Prometheus configuration
- Grafana dashboards
- Metrics collection
- Performance monitoring

### 📁 Models (`models/`)
Trained model artifacts:
- Best model (Random Forest)
- Preprocessing scaler
- Feature metadata
- Performance metrics

## File Counts

- **Total Files:** 50+
- **Python Files:** 20+
- **Configuration Files:** 15+
- **Documentation Files:** 10+
- **Test Files:** 3
- **Scripts:** 4

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

1. **Explore:** Start with README.md
2. **Setup:** Follow QUICKSTART.md
3. **Verify:** Run verify_setup.py
4. **Train:** Execute scripts/train_model.py
5. **Deploy:** Use Docker or Kubernetes guides

---



