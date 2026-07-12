# Model Deployment Architecture

## Overview

This project uses a **separation of concerns** approach for model deployment:

1. **MLflow Pod**: Contains ALL trained models and experiments for visualization and comparison
2. **API Docker Container**: Contains ONLY the best model for production serving

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Training Phase (Local)                       │
├─────────────────────────────────────────────────────────────────┤
│  python scripts/train_model.py                                   │
│                                                                   │
│  Trains 2 models → Saves 3 files:                               │
│  ✓ logistic_regression.pkl     (Individual model)               │
│  ✓ random_forest.pkl            (Individual model)               │
│  ✓ best_model.pkl               (Best performing model)          │
│  ✓ scaler.pkl                   (Feature scaler)                 │
│  ✓ metrics.json                 (All metrics)                    │
│  ✓ feature_names.json           (Feature metadata)               │
│                                                                   │
│  Logs to MLflow:                                                 │
│  ✓ mlruns_training/1/models/    (2 experiment runs)             │
│     - Run 1: Logistic Regression (params, metrics, .skops)      │
│     - Run 2: Random Forest (params, metrics, .skops)            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│    MLflow Pod (Kubernetes)    │   │   API Pod (Docker/Kubernetes) │
├───────────────────────────────┤   ├───────────────────────────────┤
│  Purpose: Visualization       │   │  Purpose: Production Serving  │
│           & Comparison         │   │                               │
│                                │   │                               │
│  Contains:                     │   │  Contains:                    │
│  ✓ mlruns_training/           │   │  ✓ best_model.pkl            │
│    - Experiment 1 (LR)         │   │  ✓ scaler.pkl                │
│    - Experiment 2 (RF)         │   │  ✓ feature_names.json        │
│    - Parameters                │   │  ✓ metrics.json              │
│    - Metrics (all)             │   │                               │
│    - Model artifacts           │   │  API loads ONLY best_model:  │
│  ✓ best_model.pkl              │   │  ```python                   │
│  ✓ scaler.pkl                  │   │  model = joblib.load(        │
│  ✓ metrics.json                │   │    "models/best_model.pkl"   │
│  ✓ feature_names.json          │   │  )                           │
│                                │   │  ```                          │
│  Memory: 3GB                   │   │                               │
│  Storage: 5GB PVC              │   │  Memory: 256Mi               │
│  Port: 30050 (NodePort)        │   │  CPU: 200m                   │
│                                │   │  Port: 30080 (NodePort)      │
│  UI: http://localhost:30050    │   │  API: http://localhost:30080 │
└───────────────────────────────┘   └───────────────────────────────┘
```

## Deployment Flow

### 1. Training (Local Development)

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Train models - generates ALL files
python scripts/train_model.py
```

**Output:**
```
models/
├── logistic_regression.pkl    # Individual LR model (optional)
├── random_forest.pkl           # Individual RF model (optional)
├── best_model.pkl              # BEST model (used by API) ✓
├── scaler.pkl                  # Feature scaler ✓
├── feature_names.json          # Feature metadata ✓
└── metrics.json                # All model metrics ✓

mlruns_training/1/models/
├── m-<run_id_1>/              # Logistic Regression run
│   ├── params/model_type      # "LogisticRegression"
│   ├── metrics/accuracy       # 0.8361
│   └── artifacts/model.skops  # Serialized model
└── m-<run_id_2>/              # Random Forest run
    ├── params/model_type      # "RandomForest"
    ├── metrics/accuracy       # 0.8525
    └── artifacts/model.skops  # Serialized model
```

### 2. MLflow Deployment (Kubernetes)

```bash
# Deploy MLflow UI server
.\scripts\deploy-mlflow.ps1
```

**What gets uploaded:**
- ✅ **mlruns_training/** - All experiment data
  - 2 complete runs (Logistic Regression + Random Forest)
  - Parameters for each model
  - Metrics for each model (accuracy, precision, recall, f1, roc_auc)
  - Model artifacts (.skops format)
  - Conda/Python environment specs
  
- ✅ **models/best_model.pkl** - For reference in MLflow UI
- ✅ **models/scaler.pkl** - Feature preprocessing info
- ✅ **models/metrics.json** - Combined metrics
- ✅ **models/feature_names.json** - Feature list

**Access:** http://localhost:30050

**What you can view:**
- 📊 Compare Logistic Regression vs Random Forest side-by-side
- 📈 View all metrics (accuracy, precision, recall, f1, ROC-AUC)
- 🔍 Inspect hyperparameters (n_estimators, random_state, etc.)
- 📦 Download model artifacts
- 📉 Visualize metric trends over time

### 3. API Deployment (Docker → Kubernetes)

#### Build Docker Image

```bash
# Build image - copies models/ directory
docker build -t heart-disease-api:latest .
```

**What gets copied (Dockerfile line 45-51):**
```dockerfile
# Copy all trained models:
# - logistic_regression.pkl (Logistic Regression model)
# - random_forest.pkl (Random Forest model)
# - best_model.pkl (Best performing model) ← API USES THIS
# - scaler.pkl (Feature scaler) ← API USES THIS
# - feature_names.json (Feature metadata)
# - metrics.json (Model metrics for all models)
COPY models/ ./models/
```

**Note:** Although all files are copied to the Docker image, the API **loads and uses ONLY** `best_model.pkl`:

```python
# api/routers/predict.py
model = joblib.load(os.path.join(MODEL_PATH, "best_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_PATH, "scaler.pkl"))
```

#### Deploy to Kubernetes

```bash
# Push to registry
docker tag heart-disease-api:latest <registry>/heart-disease-api:latest
docker push <registry>/heart-disease-api:latest

# Deploy
kubectl apply -f k8s/deployment-local.yaml
```

**Access:** http://localhost:30080/docs

## Verification

### Verify MLflow Pod Contents

```bash
# Check MLflow pod
kubectl exec -it deployment/mlflow -- sh

# Inside pod - check experiments
ls -la /mlflow/mlruns_training/1/models/
# Output:
# m-<run_id_1>/  (Logistic Regression)
# m-<run_id_2>/  (Random Forest)

# Check model files
ls -la /mlflow/models/
# Output:
# best_model.pkl
# scaler.pkl
# metrics.json
# feature_names.json
```

### Verify API Pod Contents

```bash
# Check API pod
kubectl exec -it deployment/heart-disease-api -- sh

# Inside pod - check models directory
ls -la /app/models/
# Output:
# best_model.pkl      ← Used by API
# scaler.pkl          ← Used by API
# feature_names.json  ← Used for validation
# metrics.json        ← Metadata only
```

### Test API Prediction

```bash
curl -X POST http://localhost:30080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

**Response shows which model was used:**
```json
{
  "prediction": 1,
  "prediction_label": "Heart Disease",
  "risk_score": 0.8234,
  "confidence": 0.8234,
  "model_info": {
    "model_name": "Random Forest",  ← The best model
    "model_type": "random_forest"
  }
}
```

## Benefits of This Architecture

### ✅ Separation of Concerns
- **MLflow Pod**: Heavy workload for visualization and analysis
- **API Pod**: Lightweight, optimized for prediction serving

### ✅ Resource Optimization
- **MLflow**: 3GB memory (handles large experiment data)
- **API**: 256Mi memory (minimal footprint for serving)

### ✅ Development Flexibility
- Train multiple models locally
- Compare in MLflow UI
- Deploy only the best to production
- No need to rebuild API to view experiments

### ✅ Model Versioning
- All training runs preserved in MLflow
- Easy to rollback to previous model
- Compare model versions side-by-side

### ✅ Production Safety
- API container is minimal and focused
- No unnecessary model files loaded
- Fast startup and prediction times

## Common Workflows

### Workflow 1: Train New Models

```bash
# 1. Train locally (generates new models)
python scripts/train_model.py

# 2. Update MLflow (upload new experiments)
.\scripts\deploy-mlflow.ps1

# 3. If best model changed, rebuild API
docker build -t heart-disease-api:latest .
docker push <registry>/heart-disease-api:latest
kubectl rollout restart deployment/heart-disease-api
```

### Workflow 2: Compare Models in MLflow

```bash
# Access MLflow UI
http://localhost:30050

# Navigate to experiment "heart_disease_prediction"
# Click "Compare" to see:
#   - Logistic Regression: accuracy=0.8361, roc_auc=0.9012
#   - Random Forest: accuracy=0.8525, roc_auc=0.9234
# Select best model for deployment
```

### Workflow 3: Rollback Model

```bash
# 1. In MLflow UI, identify previous best run
# 2. Download model artifact from MLflow
# 3. Replace models/best_model.pkl locally
# 4. Rebuild Docker image
docker build -t heart-disease-api:rollback .
# 5. Redeploy
kubectl set image deployment/heart-disease-api \
  api=<registry>/heart-disease-api:rollback
```

## Resource Requirements

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
|-----------|-------------|-----------|----------------|--------------|---------|
| MLflow    | 200m        | 1000m     | 1Gi            | **3Gi**      | 5Gi PVC |
| API       | 100m        | 500m      | 128Mi          | 256Mi        | N/A     |

## File Size Reference

```
models/
├── best_model.pkl         ~490 KB  (Random Forest - 100 trees)
├── logistic_regression.pkl ~8 KB   (Linear model)
├── random_forest.pkl      ~490 KB  (Same as best if RF wins)
├── scaler.pkl             ~1 KB    (StandardScaler)
├── feature_names.json     ~126 B   (13 features)
└── metrics.json           ~236 B   (All metrics)

mlruns_training/
└── 1/models/
    ├── m-<run_id_1>/      ~50 KB   (LR with metadata)
    └── m-<run_id_2>/      ~520 KB  (RF with metadata)
```

## Summary

✅ **MLflow Pod**:
- Contains: ALL models + experiments + metrics
- Purpose: Visualization, comparison, analysis
- Memory: 3GB
- Access: http://localhost:30050

✅ **API Pod**:
- Contains: ONLY best_model.pkl + artifacts
- Purpose: Production predictions
- Memory: 256Mi
- Access: http://localhost:30080

✅ **Docker Image**:
- Copies: All files from models/ directory
- Uses: Only best_model.pkl at runtime
- Size: Optimized for production

This architecture ensures **efficient resource usage**, **fast API response times**, and **comprehensive model tracking** without compromising production performance! 🚀
