# Cleanup deployment from Rancher Desktop Kubernetes
# This script removes the heart disease prediction API from your local cluster

Write-Host "🧹 Cleaning up Heart Disease API deployment..." -ForegroundColor Cyan
Write-Host ""

# Check if kubectl is available
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl not found." -ForegroundColor Red
    exit 1
}

# Navigate to the k8s directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$k8sPath = Join-Path (Split-Path -Parent $scriptPath) "k8s"

Write-Host "🗑️  Deleting Kubernetes resources..." -ForegroundColor Yellow

# Delete Deployment and Service
kubectl delete -f "$k8sPath\deployment.yaml" --ignore-not-found=true

# Delete ConfigMap
kubectl delete -f "$k8sPath\configmap.yaml" --ignore-not-found=true

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""

# Verify cleanup
Write-Host "📊 Remaining pods (should be empty):" -ForegroundColor Cyan
kubectl get pods -l app=heart-disease-api

Write-Host ""
Write-Host "✨ All resources have been removed from the cluster." -ForegroundColor Green
