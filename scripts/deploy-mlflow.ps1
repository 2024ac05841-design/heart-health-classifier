<#
.SYNOPSIS
    Deploy MLflow UI server to Kubernetes
#>

Write-Host ""
Write-Host "================================================================"
Write-Host "    MLflow Kubernetes Deployment"
Write-Host "================================================================"
Write-Host ""

# Check if mlruns_training exists
if (-not (Test-Path "mlruns_training")) {
    Write-Host "ERROR: mlruns_training/ directory not found" -ForegroundColor Red
    Write-Host "Run training first: python scripts/train_model.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Deploying MLflow to Kubernetes..." -ForegroundColor Yellow
kubectl apply -f k8s/mlflow.yaml

Write-Host ""
Write-Host "Step 2: Waiting for MLflow pod to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Wait for pod to be running
$timeout = 60
$elapsed = 0
while ($elapsed -lt $timeout) {
    $podStatus = kubectl get pods -l app=mlflow -o jsonpath='{.items[0].status.phase}' 2>$null
    if ($podStatus -eq "Running") {
        Write-Host "  OK MLflow pod is running" -ForegroundColor Green
        break
    }
    Write-Host "  Waiting for pod... ($elapsed/$timeout seconds)" -ForegroundColor Gray
    Start-Sleep -Seconds 5
    $elapsed += 5
}

if ($elapsed -ge $timeout) {
    Write-Host ""
    Write-Host "WARNING: Pod may still be starting" -ForegroundColor Yellow
    Write-Host "Check with: kubectl get pods -l app=mlflow" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Continuing with data sync..." -ForegroundColor Yellow
} else {
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "Step 3: Uploading experiment data to MLflow pod..." -ForegroundColor Yellow

# Get the pod name
$podName = kubectl get pods -l app=mlflow -o jsonpath='{.items[0].metadata.name}' 2>$null

if (-not $podName) {
    Write-Host ""
    Write-Host "ERROR: Could not find MLflow pod" -ForegroundColor Red
    Write-Host "Check deployment: kubectl get pods -l app=mlflow" -ForegroundColor Yellow
    exit 1
}

Write-Host "  Pod name: $podName" -ForegroundColor Gray

# Create archive
Write-Host ""
Write-Host "  Creating archive..." -ForegroundColor Gray
$tempArchive = "mlruns_training.tar"
if (Test-Path $tempArchive) {
    Remove-Item $tempArchive -Force
}

tar -cf $tempArchive mlruns_training/
Write-Host "  OK Archive created" -ForegroundColor Green

# Copy to pod
Write-Host ""
Write-Host "  Copying data to pod..." -ForegroundColor Gray
kubectl cp $tempArchive "default/${podName}:/tmp/mlruns_training.tar"

# Extract in pod
Write-Host "  Extracting in pod..." -ForegroundColor Gray
kubectl exec $podName -- sh -c "cd /mlflow; tar -xf /tmp/mlruns_training.tar; rm /tmp/mlruns_training.tar"

# Clean up
Remove-Item $tempArchive -Force
Write-Host "  OK Data uploaded!" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: MLflow UI is ready!" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================"
Write-Host "    ACCESS MLFLOW UI"
Write-Host "================================================================"
Write-Host ""
Write-Host "External Access:" -ForegroundColor Yellow
Write-Host "  http://localhost:30050" -ForegroundColor Cyan
Write-Host ""
Write-Host "What You Can View:" -ForegroundColor Yellow
Write-Host "  - All training runs and experiments"
Write-Host "  - Parameters: model_type n_estimators test_size random_state"
Write-Host "  - Metrics: accuracy precision recall f1 roc_auc"
Write-Host "  - Model artifacts and environment specs"
Write-Host "  - Compare multiple runs side-by-side"
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  View logs:    kubectl logs -f deployment/mlflow"
Write-Host "  Check status: kubectl get pods -l app=mlflow"
Write-Host "  Delete:       kubectl delete -f k8s/mlflow.yaml"
Write-Host ""
Write-Host "================================================================"
Write-Host ""

# Open browser
Write-Host "Opening MLflow UI..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
Start-Process http://localhost:30050
