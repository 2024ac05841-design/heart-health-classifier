# Deploy to Local Rancher Desktop Kubernetes
# This script deploys the heart disease prediction API to your local Rancher Desktop cluster

Write-Host "🚀 Deploying Heart Disease API to Rancher Desktop Kubernetes..." -ForegroundColor Cyan
Write-Host ""

# Check if kubectl is available
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl not found. Please ensure Rancher Desktop is installed and kubectl is in your PATH." -ForegroundColor Red
    exit 1
}

# Check if Kubernetes is running
Write-Host "Checking Kubernetes cluster status..." -ForegroundColor Yellow
$context = kubectl config current-context 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Cannot connect to Kubernetes. Please ensure Rancher Desktop is running." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Connected to context: $context" -ForegroundColor Green
Write-Host ""

# Navigate to the k8s directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$k8sPath = Join-Path (Split-Path -Parent $scriptPath) "k8s"

Write-Host "📦 Applying Kubernetes manifests..." -ForegroundColor Yellow

# Apply ConfigMap
Write-Host "  → Applying ConfigMap..." -ForegroundColor Cyan
kubectl apply -f "$k8sPath\configmap.yaml"

# Apply Deployment and Service
Write-Host "  → Applying Deployment and Service..." -ForegroundColor Cyan
kubectl apply -f "$k8sPath\deployment.yaml"

Write-Host ""
Write-Host "⏳ Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl rollout status deployment/heart-disease-api --timeout=5m

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""

# Get service information
Write-Host "📊 Service Information:" -ForegroundColor Cyan
kubectl get service heart-disease-api-service

Write-Host ""
Write-Host "🔍 Pod Status:" -ForegroundColor Cyan
kubectl get pods -l app=heart-disease-api

Write-Host ""
Write-Host "🌐 Access Information:" -ForegroundColor Yellow
Write-Host "  API URL: http://localhost:30080" -ForegroundColor Green
Write-Host "  Health Check: http://localhost:30080/health" -ForegroundColor Green
Write-Host "  API Docs: http://localhost:30080/docs" -ForegroundColor Green
Write-Host "  Prediction: POST http://localhost:30080/predict" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Useful Commands:" -ForegroundColor Cyan
Write-Host "  View logs: kubectl logs -l app=heart-disease-api --tail=50" -ForegroundColor White
Write-Host "  View pods: kubectl get pods -l app=heart-disease-api" -ForegroundColor White
Write-Host "  Delete deployment: kubectl delete -f k8s/deployment.yaml" -ForegroundColor White
Write-Host "  Port forward: kubectl port-forward service/heart-disease-api-service 8080:80" -ForegroundColor White

Write-Host ""
Write-Host "🧪 Test the API:" -ForegroundColor Yellow
Write-Host "  curl http://localhost:30080/health" -ForegroundColor White
Write-Host '  curl -X POST http://localhost:30080/predict -H "Content-Type: application/json" -d @test_data.json' -ForegroundColor White
