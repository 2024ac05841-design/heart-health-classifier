#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Extract individual models from MLflow experiments to models/ directory
.DESCRIPTION
    This script extracts the Logistic Regression and Random Forest models
    from MLflow experiment runs and copies them to the models/ directory,
    ensuring the Docker image contains all trained models.
#>

Write-Host ""
Write-Host "================================================================"
Write-Host "    Extract Individual Models from MLflow"
Write-Host "================================================================"
Write-Host ""

# Check if mlruns_training exists
if (-not (Test-Path "mlruns_training\1\models")) {
    Write-Host "ERROR: MLflow experiments not found" -ForegroundColor Red
    Write-Host "Run training first: python scripts/train_model.py" -ForegroundColor Yellow
    exit 1
}

# Get list of model runs
$modelRuns = Get-ChildItem "mlruns_training\1\models" -Directory

if ($modelRuns.Count -lt 2) {
    Write-Host "ERROR: Expected 2 model runs but found $($modelRuns.Count)" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($modelRuns.Count) model runs in MLflow" -ForegroundColor Green
Write-Host ""

# Read metrics to determine which is which
$models = @()
foreach ($run in $modelRuns) {
    $metricsPath = Join-Path $run.FullName "metrics"
    $paramsPath = Join-Path $run.FullName "params"
    
    if (Test-Path $paramsPath) {
        $modelTypeFile = Join-Path $paramsPath "model_type"
        if (Test-Path $modelTypeFile) {
            $modelType = Get-Content $modelTypeFile -Raw | ForEach-Object { $_.Trim() }
            $artifactPath = Join-Path $run.FullName "artifacts\model.skops"
            
            $models += [PSCustomObject]@{
                RunId = $run.Name
                ModelType = $modelType
                ArtifactPath = $artifactPath
            }
            
            Write-Host "  Run: $($run.Name)" -ForegroundColor Gray
            Write-Host "    Model Type: $modelType" -ForegroundColor White
        }
    }
}

Write-Host ""
Write-Host "Copying individual models to models/ directory..." -ForegroundColor Yellow
Write-Host ""

# Ensure models directory exists
if (-not (Test-Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
}

# Copy each model
foreach ($model in $models) {
    $destFile = ""
    if ($model.ModelType -eq "LogisticRegression") {
        $destFile = "models\logistic_regression.pkl"
    } elseif ($model.ModelType -eq "RandomForest") {
        $destFile = "models\random_forest.pkl"
    } else {
        Write-Host "  WARNING: Unknown model type: $($model.ModelType)" -ForegroundColor Yellow
        continue
    }
    
    if (Test-Path $model.ArtifactPath) {
        Copy-Item -Path $model.ArtifactPath -Destination $destFile -Force
        $fileSize = (Get-Item $destFile).Length
        Write-Host "  OK Copied $($model.ModelType) -> $destFile ($([math]::Round($fileSize/1KB, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Model artifact not found: $($model.ArtifactPath)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Verifying models/ directory..." -ForegroundColor Yellow
Write-Host ""

$expectedFiles = @(
    "logistic_regression.pkl",
    "random_forest.pkl",
    "best_model.pkl",
    "scaler.pkl",
    "feature_names.json",
    "metrics.json"
)

$allPresent = $true
foreach ($file in $expectedFiles) {
    $path = "models\$file"
    if (Test-Path $path) {
        $size = (Get-Item $path).Length
        Write-Host "  [OK] $file ($([math]::Round($size/1KB, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ""
Write-Host "================================================================"
Write-Host "    Summary"
Write-Host "================================================================"
Write-Host ""

if ($allPresent) {
    Write-Host "SUCCESS: All models are ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The models/ directory now contains:" -ForegroundColor Yellow
    Write-Host "  - logistic_regression.pkl (Logistic Regression model)" -ForegroundColor White
    Write-Host "  - random_forest.pkl (Random Forest model)" -ForegroundColor White
    Write-Host "  - best_model.pkl (Best performing model)" -ForegroundColor White
    Write-Host "  - scaler.pkl (Feature scaler)" -ForegroundColor White
    Write-Host "  - feature_names.json (Feature metadata)" -ForegroundColor White
    Write-Host "  - metrics.json (Model metrics)" -ForegroundColor White
    Write-Host ""
    Write-Host "When you build the Docker image, ALL models will be included:" -ForegroundColor Cyan
    Write-Host "  docker build -t heart-disease-api ." -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "WARNING: Some files are missing" -ForegroundColor Yellow
    Write-Host "Consider retraining: python scripts/train_model.py" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "================================================================"
Write-Host ""
