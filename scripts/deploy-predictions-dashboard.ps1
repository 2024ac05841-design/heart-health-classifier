# PowerShell script to deploy the Grafana Predictions Dashboard
# For Windows/Rancher Desktop environments

Write-Host "`n🎯 Deploying Heart Disease Predictions Dashboard to Grafana...`n" -ForegroundColor Cyan

# Check if kubectl is available
if (!(Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}

# Check if the main monitoring stack is deployed
try {
    kubectl get deployment grafana 2>$null | Out-Null
} catch {
    Write-Host "❌ Grafana deployment not found. Please deploy monitoring-local.yaml first." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Step 1: Updating Grafana configuration..." -ForegroundColor Yellow

# Redeploy monitoring with updated configuration
Write-Host "   Applying monitoring-local.yaml with Infinity plugin..." -ForegroundColor White
kubectl apply -f k8s/monitoring-local.yaml

Write-Host "`n🔄 Step 2: Loading predictions dashboard..." -ForegroundColor Yellow

# Method 1: Via Grafana API (recommended)
Write-Host "   Option A: Using Grafana HTTP API" -ForegroundColor White
Write-Host "   Waiting for Grafana to be ready..." -ForegroundColor Gray

Start-Sleep -Seconds 10

# Port-forward to Grafana
Write-Host "   Setting up port-forward to Grafana..." -ForegroundColor Gray
$portForwardJob = Start-Job -ScriptBlock {
    kubectl port-forward svc/grafana 3000:3000
}

Start-Sleep -Seconds 5

# Import dashboard via API
try {
    $dashboardJson = Get-Content "k8s\grafana-dashboard-predictions.json" -Raw | ConvertFrom-Json
    
    # Wrap in dashboard object for API
    $apiPayload = @{
        dashboard = $dashboardJson
        overwrite = $true
        message = "Automated deployment of predictions dashboard"
    } | ConvertTo-Json -Depth 100
    
    Write-Host "   Importing dashboard via API..." -ForegroundColor Gray
    
    # Use basic auth (admin:admin)
    $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin"))
    $headers = @{
        Authorization = "Basic $base64AuthInfo"
        "Content-Type" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/dashboards/db" `
        -Method Post `
        -Headers $headers `
        -Body $apiPayload `
        -ErrorAction Stop
    
    Write-Host "   ✅ Dashboard imported successfully!" -ForegroundColor Green
    Write-Host "   Dashboard UID: $($response.uid)" -ForegroundColor White
    Write-Host "   Dashboard URL: $($response.url)" -ForegroundColor White
    
} catch {
    Write-Host "   ⚠️  API import failed: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   Will use ConfigMap method instead..." -ForegroundColor Yellow
    
    # Method 2: Via ConfigMap
    Write-Host "`n   Option B: Using ConfigMap" -ForegroundColor White
    Write-Host "   Creating ConfigMap for predictions dashboard..." -ForegroundColor Gray
    
    kubectl create configmap grafana-predictions-dashboard `
        --from-file=grafana-predictions-dashboard.json=k8s\grafana-dashboard-predictions.json `
        --dry-run=client -o yaml | kubectl apply -f -
    
    Write-Host "   ✅ ConfigMap created!" -ForegroundColor Green
    Write-Host "   Note: Dashboard will be loaded on next Grafana restart" -ForegroundColor Yellow
} finally {
    # Clean up port-forward job
    if ($portForwardJob) {
        Stop-Job $portForwardJob
        Remove-Job $portForwardJob
    }
}

Write-Host "`n🔄 Step 3: Restarting Grafana to apply changes..." -ForegroundColor Yellow
kubectl rollout restart deployment/grafana

Write-Host "   Waiting for Grafana to be ready..." -ForegroundColor Gray
kubectl wait --for=condition=available --timeout=120s deployment/grafana

Write-Host "`n════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "  ✅ PREDICTIONS DASHBOARD DEPLOYMENT COMPLETE! ✅" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════`n" -ForegroundColor Gray

Write-Host "🌐 Access the dashboard at:" -ForegroundColor Cyan
Write-Host "   Main: http://localhost:30030" -ForegroundColor White
Write-Host "   Direct: http://localhost:30030/d/heart-disease-predictions/heart-disease-prediction-history`n" -ForegroundColor White

Write-Host "🔑 Default credentials:" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin`n" -ForegroundColor White

Write-Host "📊 Dashboard Features:" -ForegroundColor Cyan
Write-Host "   ✓ Total predictions count (from Redis)" -ForegroundColor Green
Write-Host "   ✓ High/Low risk distribution" -ForegroundColor Green
Write-Host "   ✓ Average risk score gauge" -ForegroundColor Green
Write-Host "   ✓ Average confidence gauge" -ForegroundColor Green
Write-Host "   ✓ Real-time prediction rate chart" -ForegroundColor Green
Write-Host "   ✓ Prediction distribution pie chart" -ForegroundColor Green
Write-Host "   ✓ Recent 50 predictions table" -ForegroundColor Green
Write-Host "   ✓ Risk score distribution histogram" -ForegroundColor Green
Write-Host "   ✓ Inference time percentiles (p50, p95, p99)`n" -ForegroundColor Green

Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "   • Dashboard auto-refreshes every 30 seconds" -ForegroundColor White
Write-Host "   • Shows data from last 15 minutes by default" -ForegroundColor White
Write-Host "   • Uses Infinity datasource to query API endpoints" -ForegroundColor White
Write-Host "   • Combines Prometheus metrics with Redis data`n" -ForegroundColor White

Write-Host "🔧 Troubleshooting:" -ForegroundColor Cyan
Write-Host "   If dashboard doesn't show data:" -ForegroundColor White
Write-Host "   1. Verify API is running: kubectl get pods -l app=heart-disease-api" -ForegroundColor Gray
Write-Host "   2. Check API logs: kubectl logs -l app=heart-disease-api" -ForegroundColor Gray
Write-Host "   3. Test endpoint: curl http://localhost:30080/api/predictions/stats" -ForegroundColor Gray
Write-Host "   4. Check Infinity plugin: Grafana → Configuration → Data Sources`n" -ForegroundColor Gray

Write-Host "════════════════════════════════════════════════════════════`n" -ForegroundColor Gray
