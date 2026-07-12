# Screenshot Guide for Project Report

This directory contains screenshots required for the comprehensive project report (`PROJECT_REPORT.md`).

## 📁 Directory Structure

```
screenshots/
├── mlflow/          # MLflow experiment tracking screenshots
├── cicd/            # GitHub Actions CI/CD pipeline screenshots
├── kubernetes/      # Kubernetes deployment screenshots
└── README.md        # This file
```

---

## 📸 Required Screenshots

### MLflow Screenshots (5 files)

**Location:** `screenshots/mlflow/`

1. **mlflow_experiments_list.png**
   - URL: http://localhost:30050
   - Capture: List of all experiments with runs
   - Shows: Experiment names, run counts, creation dates

2. **mlflow_run_details.png**
   - URL: http://localhost:30050 (click on a specific run)
   - Capture: Detailed view of the best performing run
   - Shows: Parameters, metrics, tags

3. **mlflow_metrics_comparison.png**
   - URL: http://localhost:30050 (select multiple runs)
   - Capture: Comparison chart of metrics across runs
   - Shows: Accuracy, F1-score, ROC-AUC comparison

4. **mlflow_model_registry.png**
   - URL: http://localhost:30050 (Models tab)
   - Capture: Model registry showing registered model
   - Shows: Model name "heart-disease-predictor", version, stage (Production)

5. **mlflow_artifacts.png**
   - URL: http://localhost:30050 (click run → Artifacts tab)
   - Capture: Logged artifacts (model files, plots)
   - Shows: best_model.pkl, scaler.pkl, confusion_matrix.png

---

### CI/CD Screenshots (6 files)

**Location:** `screenshots/cicd/`

1. **github_actions_workflow.png**
   - URL: https://github.com/2024ac05841-design/heart-health-classifier/actions
   - Capture: GitHub Actions tab showing workflow runs
   - Shows: CI/CD workflow status, recent runs, success/failure

2. **github_actions_tests.png**
   - URL: Click on a successful workflow run → "Test" job
   - Capture: Test execution results
   - Shows: 79 tests passed, pytest output

3. **github_actions_coverage.png**
   - URL: Same workflow run → "Upload coverage reports" step
   - Capture: Coverage reporting output
   - Shows: 89.59% coverage, statements covered

4. **github_actions_docker_build.png**
   - URL: Same workflow run → "Build Docker Image" step
   - Capture: Docker build logs
   - Shows: Build steps, layer caching, image tagging

5. **github_actions_security_scan.png**
   - URL: Same workflow run → "Trivy Security Scan" step
   - Capture: Security scan results
   - Shows: Vulnerability scan output, no critical issues

6. **codecov_dashboard.png**
   - URL: https://codecov.io (your repository)
   - Capture: Codecov coverage dashboard
   - Shows: Coverage percentage, trend graph, file coverage

---

### Kubernetes Screenshots (9 files)

**Location:** `screenshots/kubernetes/`

1. **kubectl_get_pods.png**
   - Command: `kubectl get pods`
   - Capture: Terminal output showing all 8 pods running
   - Shows: Pod names, status (Running), restarts, age

2. **kubectl_get_services.png**
   - Command: `kubectl get svc`
   - Capture: Terminal output showing all services
   - Shows: Service names, types (NodePort/ClusterIP), ports

3. **kubectl_describe_pod.png**
   - Command: `kubectl describe pod <api-pod-name>`
   - Capture: Detailed pod information
   - Shows: Image, environment variables, resource limits, events

4. **api_swagger_ui.png**
   - URL: http://localhost:30080/docs
   - Capture: FastAPI Swagger documentation page
   - Shows: API endpoints (/predict, /health, /history), schemas

5. **api_health_check.png**
   - URL: http://localhost:30080/health (or use curl/Postman)
   - Capture: Health check response
   - Shows: JSON response with status, model_loaded, redis_connected

6. **grafana_dashboard.png**
   - URL: http://localhost:30030 (login: admin/admin)
   - Capture: Main Grafana dashboard
   - Shows: Metrics panels, graphs, system statistics

7. **prometheus_targets.png**
   - URL: http://localhost:30090/targets
   - Capture: Prometheus targets page
   - Shows: All scrape targets, status (UP), last scrape time

8. **redis_cache_metrics.png**
   - URL: http://localhost:30030 → "Redis Prediction Cache" dashboard
   - Capture: Redis monitoring dashboard
   - Shows: Memory usage, keys, cache hit rate, command stats

9. **api_prediction_response.png**
   - Method: Make POST request to http://localhost:30080/predict
   - Capture: API response JSON
   - Shows: prediction, probability, risk_level, prediction_id, timestamp

---

## 🎯 How to Capture Screenshots

### For Web URLs (MLflow, Grafana, Prometheus)

1. Open the URL in your browser
2. Wait for the page to fully load
3. Use screenshot tool:
   - **Windows:** Win + Shift + S (Snipping Tool)
   - **macOS:** Cmd + Shift + 4
   - **Linux:** Shift + PrtScn (or use Flameshot)
4. Crop to relevant area (exclude browser chrome if possible)
5. Save to the appropriate directory with exact filename

### For Terminal Commands (kubectl)

1. Open PowerShell or Terminal
2. Run the command (e.g., `kubectl get pods`)
3. Take screenshot of the terminal output
4. Alternatively, use:
   ```powershell
   kubectl get pods | Out-File -FilePath screenshots/kubernetes/kubectl_get_pods.txt
   # Then take screenshot of the text file
   ```

### For GitHub Actions

1. Navigate to: https://github.com/2024ac05841-design/heart-health-classifier/actions
2. Click on the most recent successful workflow run
3. Expand each job to see detailed logs
4. Capture each required step

### For API Responses (Postman/curl)

**Using Postman:**
1. Create POST request to http://localhost:30080/predict
2. Set Content-Type: application/json
3. Add body with patient data
4. Send request
5. Capture response panel

**Using PowerShell:**
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:30080/predict" -Method Post `
  -ContentType "application/json" `
  -Body (@{
    age=63; sex=1; cp=3; trestbps=145; chol=233; fbs=1;
    restecg=0; thalach=150; exang=0; oldpeak=2.3;
    slope=0; ca=0; thal=1
  } | ConvertTo-Json)

$response | ConvertTo-Json -Depth 10
# Capture this output
```

---

## ✅ Screenshot Checklist

Use this checklist to track your progress:

### MLflow (5 screenshots)
- [ ] mlflow_experiments_list.png
- [ ] mlflow_run_details.png
- [ ] mlflow_metrics_comparison.png
- [ ] mlflow_model_registry.png
- [ ] mlflow_artifacts.png

### CI/CD (6 screenshots)
- [ ] github_actions_workflow.png
- [ ] github_actions_tests.png
- [ ] github_actions_coverage.png
- [ ] github_actions_docker_build.png
- [ ] github_actions_security_scan.png
- [ ] codecov_dashboard.png

### Kubernetes (9 screenshots)
- [ ] kubectl_get_pods.png
- [ ] kubectl_get_services.png
- [ ] kubectl_describe_pod.png
- [ ] api_swagger_ui.png
- [ ] api_health_check.png
- [ ] grafana_dashboard.png
- [ ] prometheus_targets.png
- [ ] redis_cache_metrics.png
- [ ] api_prediction_response.png

**Total:** 20 screenshots

---

## 📝 Tips for Quality Screenshots

1. **Resolution:** Use high resolution (at least 1920x1080)
2. **Clarity:** Ensure text is readable
3. **Relevant Content:** Crop to show only relevant information
4. **Annotations:** Consider adding arrows or highlights for key elements
5. **Consistency:** Use consistent capture method for all screenshots
6. **File Format:** PNG preferred (lossless), JPEG acceptable
7. **File Size:** Optimize if >2MB (use compression tools)

---

## 🔗 Quick Links

- **MLflow:** http://localhost:30050
- **API Docs:** http://localhost:30080/docs
- **Grafana:** http://localhost:30030
- **Prometheus:** http://localhost:30090
- **GitHub Actions:** https://github.com/2024ac05841-design/heart-health-classifier/actions

---

## 📄 Using Screenshots in Report

Once all screenshots are captured:

1. Place them in appropriate directories
2. Reference them in `PROJECT_REPORT.md`
3. Optionally, embed images in Markdown:
   ```markdown
   ![MLflow Experiments](screenshots/mlflow/mlflow_experiments_list.png)
   ```

4. For PDF conversion, screenshots will be automatically included

---

## 🤝 Need Help?

If you encounter issues:
- Ensure all services are running: `kubectl get pods`
- Check service accessibility: Test URLs in browser
- Verify NodePort bindings: `kubectl get svc`
- Review logs: `kubectl logs <pod-name>`

---

**Last Updated:** July 12, 2026  
**For:** PROJECT_REPORT.md comprehensive documentation
