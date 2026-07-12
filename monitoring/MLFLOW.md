# MLflow Experiment Tracking

This project uses **MLflow** for experiment tracking, model versioning, and artifact management during model training.

## 📊 What is MLflow?

MLflow is an open-source platform for managing the machine learning lifecycle, including:
- **Experiment Tracking**: Log parameters, metrics, and artifacts
- **Model Registry**: Version and manage trained models
- **Model Deployment**: Package models for deployment
- **Reproducibility**: Track environment and dependencies

## 🎯 What We Track

### 1. **Parameters**
Configuration and hyperparameters for each training run:
- `model_type`: Type of model (LogisticRegression, RandomForest)
- `n_estimators`: Number of trees (for RandomForest)
- `test_size`: Proportion of test data (default: 0.2)
- `random_state`: Random seed for reproducibility (42)

### 2. **Metrics**
Performance metrics for each model:
- `accuracy`: Overall prediction accuracy
- `precision`: Positive predictive value
- `recall`: True positive rate (sensitivity)
- `f1`: Harmonic mean of precision and recall
- `roc_auc`: Area under the ROC curve

### 3. **Models**
Trained sklearn models logged with:
- Model binary (serialized with skops)
- MLmodel file (model metadata)
- Conda environment specification
- Python environment specification
- Requirements.txt

### 4. **Artifacts**
Additional files logged:
- `conda.yaml`: Conda environment specification
- `python_env.yaml`: Python environment details
- `requirements.txt`: Python package dependencies
- `model.skops`: Serialized sklearn model

## 🏃 Running MLflow

### Option 1: Local MLflow UI (Development)

**Note**: MLflow command is not available in PATH by default. You need to activate the virtual environment first:

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
mlflow ui --port 5000 --backend-store-uri file:./mlruns_training

# Linux/Mac
source venv/bin/activate
mlflow ui --port 5000 --backend-store-uri file:./mlruns_training
```

**Alternative using Python module**:
```powershell
# Works without activating venv
python -m mlflow ui --port 5000 --backend-store-uri file:./mlruns_training
```

Then visit: **http://localhost:5000**

### Option 2: MLflow in Kubernetes (Recommended)

Deploy MLflow as a pod to visualize experiments in your cluster:

```powershell
# Windows PowerShell
.\scripts\deploy-mlflow.ps1

# Linux/Mac
bash scripts/deploy-mlflow.sh
```

This will:
1. Deploy MLflow UI server as a Kubernetes pod
2. Upload your local `mlruns_training/` data to the pod
3. Expose MLflow UI at **http://localhost:30050**

**Access**: http://localhost:30050

## 🔍 Viewing Experiments

### In MLflow UI

1. **Experiments Page**
   - Lists all experiments (heart_disease_prediction)
   - Shows run count and creation time

2. **Runs Table**
   - Compare multiple training runs side-by-side
   - Sort by any metric (accuracy, ROC-AUC, etc.)
   - Filter runs by parameters or metrics
   - View run details

3. **Run Details**
   - **Parameters**: All hyperparameters used
   - **Metrics**: Performance metrics with graphs
   - **Artifacts**: Download model files, environment specs
   - **System Info**: Execution time, user, source

4. **Compare Runs**
   - Select multiple runs to compare
   - Parallel coordinates plot
   - Scatter plot matrix
   - Side-by-side metric comparison

## 📁 Directory Structure

```
mlruns_training/              # Local MLflow tracking directory
├── 1/                        # Experiment ID
│   ├── meta.yaml            # Experiment metadata
│   └── models/              # Model runs
│       ├── m-<run_id_1>/   # Run 1 (e.g., Logistic Regression)
│       │   ├── artifacts/
│       │   │   ├── conda.yaml
│       │   │   ├── MLmodel
│       │   │   ├── model.skops
│       │   │   ├── python_env.yaml
│       │   │   └── requirements.txt
│       │   ├── metrics/     # Metric values
│       │   ├── params/      # Parameter values
│       │   └── tags/        # Run tags
│       └── m-<run_id_2>/   # Run 2 (e.g., Random Forest)
│           └── ...
└── mlflow.db                # SQLite tracking database
```

## 🧪 Training with MLflow

When you run training, MLflow automatically logs everything:

```bash
python scripts/train_model.py
```

**What happens**:
1. Creates experiment "heart_disease_prediction"
2. Starts two runs (Logistic Regression + Random Forest)
3. Logs parameters for each model
4. Logs metrics after evaluation
5. Saves model artifacts
6. Stores everything in `mlruns_training/`

## 🚀 Advanced Usage

### Custom Experiment Name
```bash
python scripts/train_model.py --experiment-name my_custom_experiment
```

### Programmatic Access
```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("file:./mlruns_training")

# Set experiment
mlflow.set_experiment("heart_disease_prediction")

# Start a run
with mlflow.start_run(run_name="my_model"):
    # Log parameters
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.85)
    mlflow.log_metric("roc_auc", 0.90)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("path/to/file.txt")
```

### Query Runs Programmatically
```python
from mlflow.tracking import MlflowClient

client = MlflowClient(tracking_uri="file:./mlruns_training")

# Get experiment
experiment = client.get_experiment_by_name("heart_disease_prediction")

# Get all runs
runs = client.search_runs(experiment_ids=[experiment.experiment_id])

# Get best run by ROC-AUC
best_run = max(runs, key=lambda r: r.data.metrics.get("roc_auc", 0))
print(f"Best model: {best_run.data.params['model_type']}")
print(f"ROC-AUC: {best_run.data.metrics['roc_auc']}")
```

## 🐳 Kubernetes Deployment Details

### Resources
- **CPU**: 100m request, 500m limit
- **Memory**: 256Mi request, 512Mi limit
- **Storage**: 5Gi persistent volume

### Services
- **mlflow-service** (NodePort): External access at port 30050
- **mlflow** (ClusterIP): Internal cluster access at port 5000

### Health Checks
- **Liveness Probe**: HTTP GET /health every 10s
- **Readiness Probe**: HTTP GET /health every 5s

### Data Persistence
- Uses PersistentVolumeClaim (`mlflow-data-pvc`)
- Data survives pod restarts
- Initial data copied from local `mlruns_training/`

## 🔧 Useful Commands

### Local MLflow
```bash
# Start UI (with venv activated)
mlflow ui --port 5000 --backend-store-uri file:./mlruns_training

# Start UI (without venv)
python -m mlflow ui --port 5000 --backend-store-uri file:./mlruns_training
```

### Kubernetes MLflow
```bash
# Deploy MLflow
kubectl apply -f k8s/mlflow.yaml

# Check status
kubectl get pods -l app=mlflow
kubectl get svc mlflow-service

# View logs
kubectl logs -f deployment/mlflow

# Port forward (alternative access)
kubectl port-forward svc/mlflow-service 5000:5000

# Delete MLflow
kubectl delete -f k8s/mlflow.yaml
```

### Sync Updated Data
If you run more training locally and want to update Kubernetes:
```powershell
# Windows
.\scripts\deploy-mlflow.ps1

# Linux/Mac
bash scripts/deploy-mlflow.sh
```

## 📊 Example Workflow

1. **Train models locally**:
   ```bash
   python scripts/train_model.py
   ```

2. **View experiments locally** (optional):
   ```bash
   python -m mlflow ui --port 5000 --backend-store-uri file:./mlruns_training
   ```

3. **Deploy MLflow to Kubernetes**:
   ```powershell
   .\scripts\deploy-mlflow.ps1
   ```

4. **Access MLflow UI**:
   - Open: http://localhost:30050
   - View all experiments and runs
   - Compare model performance
   - Download model artifacts

5. **Analyze results**:
   - Sort runs by ROC-AUC
   - Compare parameters between models
   - Visualize metric trends
   - Export best model

## 🎯 Benefits

✅ **Reproducibility**: Every run is tracked with exact parameters
✅ **Comparison**: Easily compare multiple model variants
✅ **Versioning**: Track model evolution over time
✅ **Collaboration**: Team members can view all experiments
✅ **Deployment**: Package models with dependencies for deployment

## 🐛 Troubleshooting

### MLflow command not found
**Issue**: `mlflow: command not found` or `The term 'mlflow' is not recognized`

**Solution**:
```powershell
# Option 1: Activate virtual environment
.\venv\Scripts\Activate.ps1
mlflow ui --port 5000

# Option 2: Use Python module directly (recommended)
python -m mlflow ui --port 5000 --backend-store-uri file:./mlruns_training
```

### No experiments visible
**Issue**: MLflow UI shows no experiments

**Solution**: Verify tracking URI points to correct directory
```bash
# Check if mlruns_training exists
ls mlruns_training/

# Use correct backend store URI
mlflow ui --backend-store-uri file:./mlruns_training
```

### Kubernetes pod not starting
**Issue**: MLflow pod stuck in pending or error state

**Solution**:
```bash
# Check pod status
kubectl describe pod -l app=mlflow

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# View logs
kubectl logs -l app=mlflow
```

## 📚 Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
- [MLflow Models](https://mlflow.org/docs/latest/models.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/index.html)
