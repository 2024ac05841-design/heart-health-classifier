# 📊 Monitoring Stack

This directory contains monitoring configurations for the Heart Disease Prediction API using Prometheus and Grafana.

## 🚀 Quick Start

### Deploy Monitoring Stack on Kubernetes

```bash
# Deploy Prometheus and Grafana
kubectl apply -f k8s/monitoring-local.yaml

# Deploy Loki for log aggregation
kubectl apply -f k8s/loki-stack.yaml

# Check deployment status
kubectl get pods -l app=prometheus
kubectl get pods -l app=grafana
kubectl get pods -l app=loki
kubectl get pods -l app=promtail

# View services
kubectl get svc prometheus
kubectl get svc grafana
kubectl get svc loki
```

### Access Dashboards

Once deployed, access the monitoring dashboards:

- **Prometheus UI**: http://localhost:30090
- **Grafana Dashboards**: http://localhost:30030
  - Username: `admin`
  - Password: `admin`
  - **Metrics Dashboard**: "Heart Disease Prediction API - ML Monitoring"
  - **Logs Dashboard**: "Heart Disease API - Logs & Filtering"

## 📈 Setting Up Grafana

### 1. Add Prometheus Data Source

1. Open Grafana at http://localhost:30030
2. Log in with `admin/admin`
3. Go to **Configuration** → **Data Sources**
4. Click **Add data source**
5. Select **Prometheus**
6. Set URL to: `http://prometheus:9090`
7. Click **Save & Test**

### 2. Dashboard Auto-Loaded! 🎉

**Good news:** The dashboard is automatically provisioned when you deploy the monitoring stack!

When you run `kubectl apply -f k8s/monitoring-local.yaml`, Grafana will:
- ✅ Automatically configure Prometheus as a datasource
- ✅ Automatically load the Heart Disease API dashboard
- ✅ Persist the dashboard (no need to re-import after restart)

**Just log in and it's ready:**
1. Open http://localhost:30030
2. Log in with **admin/admin**
3. Go to **Dashboards** → **Heart Disease Prediction API - ML Monitoring**
4. Done! The dashboard is already configured with all metrics.

**Dashboard includes:**
- 📊 Model Status & Health
- 🚀 Request Rate & Latency
- 🎯 Prediction Distribution (Disease vs No Disease)
- 📈 Risk Level Distribution (High/Medium/Low)
- ⚡ Model Inference Time (p50, p95, p99)
- 🔍 Prediction Confidence Tracking
- 💾 Memory & CPU Usage
- 📉 Error Rate Monitoring

The dashboard auto-refreshes every 10 seconds and shows the last hour of data.

**Want to customize?** The dashboard allows UI updates, so you can:
- Add new panels
- Modify existing visualizations  
- Change time ranges and refresh rates
- Export your customized version

Your changes will persist across pod restarts!

### 3. Logs Dashboard - Filter & Search 🔍

The **Logs Dashboard** provides real-time log filtering and search capabilities powered by Loki.

**Access:** Dashboards → "Heart Disease API - Logs & Filtering"

**Features:**
- 📊 **Log Volume Graph**: Visual timeline of log levels (INFO, WARNING, ERROR)
- 🚨 **Error Logs Panel**: Auto-filtered for errors, exceptions, and failures
- 🎯 **Prediction Logs Panel**: Shows all prediction-related logs
- 🤖 **Model & Artifacts Logs**: Tracks model loading, artifacts, scaler info
- 📊 **Performance Metrics Logs**: Displays confidence, risk, inference time logs
- 📝 **Live Stream**: All application logs in real-time

**Search & Filter:**
- Use the **Search** box at the top to filter logs by any keyword
- Select **Log Level** dropdown to filter by INFO, WARNING, ERROR, CRITICAL
- Click on any log line to expand details
- All panels auto-refresh every 10 seconds

**Common Searches:**
- Error patterns: Pre-filtered in Error Logs panel
- Prediction logs: `Prediction:` or `predict`
- Model status: `model`, `loaded`, `artifact`, `scaler`
- Performance: `confidence`, `risk`, `inference`, `preprocess`

**Tip:** The logs dashboard works best after making some predictions to generate log data!

#### Manual Import (if needed)

If you want to import the dashboard manually or on a different Grafana instance:

1. In Grafana, click **Dashboards** → **Import**
2. Click **Upload JSON file**
3. Select `monitoring/grafana-dashboard.json`
4. Select your Prometheus data source
5. Click **Import**

#### Create Additional Custom Panels

If you want to build your own panels, use these PromQL queries:

**API Performance:**
```promql
# Request rate
rate(http_requests_total[5m])

# Response time percentiles
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

**ML Predictions:**
```promql
# Prediction rate by class
rate(heart_disease_predictions_total[5m])

# Average confidence
rate(heart_disease_prediction_confidence_sum[5m]) / rate(heart_disease_prediction_confidence_count[5m])

# Risk score distribution
histogram_quantile(0.50, rate(heart_disease_risk_score_bucket[5m]))
```

**Model Performance:**
```promql
# Inference time
histogram_quantile(0.95, rate(model_inference_seconds_bucket[5m]))

# Preprocessing time
histogram_quantile(0.95, rate(data_preprocessing_seconds_bucket[5m]))

# Model loaded status
model_loaded_status
```

**System Resources:**
```promql
# Memory usage
process_resident_memory_bytes

# CPU time
rate(process_cpu_seconds_total[5m])
```

## 🔔 Alerting

Alerts are automatically configured via the ConfigMap in `k8s/monitoring-local.yaml`.

View active alerts in Prometheus UI:
- **Alerts**: http://localhost:30090/alerts

### Configured Alerts

| Alert | Severity | Threshold |
|-------|----------|-----------|
| HighErrorRate | Critical | 5xx errors > 5% |
| SlowAPIResponses | Warning | p95 latency > 1s |
| ModelNotLoaded | Critical | Model status = 0 |
| LowPredictionConfidence | Warning | Avg confidence < 60% |
| HighPredictionVolume | Info | > 100 req/sec |
| APIServiceDown | Critical | Service unreachable |

## 📝 Files

- **prometheus.yml**: Standalone Prometheus config (for reference)
- **alerts.yml**: Alerting rules (for reference, actual rules in k8s ConfigMap)
- **k8s/monitoring-local.yaml**: Complete K8s deployment with Prometheus + Grafana

## 🔧 Customization

### Update Scrape Interval

Edit the ConfigMap in `k8s/monitoring-local.yaml`:

```yaml
data:
  prometheus.yml: |
    scrape_configs:
      - job_name: 'heart-disease-api'
        scrape_interval: 10s  # Change this
```

Then reapply:
```bash
kubectl apply -f k8s/monitoring-local.yaml
kubectl rollout restart deployment/prometheus
```

### Add More Alerts

Edit the alerts section in the ConfigMap and reapply.

## 🧹 Cleanup

To remove the monitoring stack:

```bash
kubectl delete -f k8s/monitoring-local.yaml
```

## 📊 Sample Grafana Dashboard Queries

### Panel 1: Request Rate
- **Type**: Graph
- **Query**: `rate(http_requests_total[5m])`
- **Legend**: `{{method}} {{handler}}`

### Panel 2: Prediction Distribution
- **Type**: Pie Chart
- **Query**: `sum by (prediction_class) (rate(heart_disease_predictions_total[5m]))`

### Panel 3: Response Time
- **Type**: Graph
- **Queries**:
  - p50: `histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))`
  - p95: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
  - p99: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`

### Panel 4: Confidence Score
- **Type**: Gauge
- **Query**: `avg(rate(heart_disease_prediction_confidence_sum[5m]) / rate(heart_disease_prediction_confidence_count[5m]))`
- **Min**: 0, **Max**: 1

### Panel 5: Model Inference Time
- **Type**: Graph
- **Query**: `histogram_quantile(0.95, rate(model_inference_seconds_bucket[5m])) * 1000`
- **Unit**: milliseconds

## 🎯 Best Practices

1. **Monitor What Matters**: Focus on metrics that indicate service health and ML model performance
2. **Set Meaningful Alerts**: Avoid alert fatigue by setting appropriate thresholds
3. **Regular Review**: Check dashboards regularly and adjust queries as needed
4. **Resource Limits**: Monitor Prometheus memory usage, increase limits if needed
5. **Data Retention**: Configure retention period based on your needs (default: 15 days)

## 📚 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
