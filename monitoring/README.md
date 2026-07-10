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
- **Grafana Dashboards**: http://localhost:30030 (Login: admin/admin)

## 📊 Available Dashboards

All dashboards are automatically provisioned and ready to use:

### 🏠 Infrastructure Overview - System Health (Home Page)
Infrastructure health dashboard showing real-time status, resource usage, and metrics for all monitoring pods.

**16 Panels:**
- Pod status indicators (Heart API, Prometheus, Grafana, Loki, Promtail)
- Memory usage per pod and total
- CPU usage trends
- Request rates
- Uptime tracking

### 1. Heart Disease Prediction API - ML Monitoring
Main monitoring dashboard with 14 panels tracking API performance and ML metrics.

### 2. Heart Disease API - Advanced Metrics  
Advanced analysis dashboard with 11 panels for data drift detection and pipeline performance.

### 3. Heart Disease API - Logs & Filtering
Log aggregation dashboard with 6 panels for real-time log filtering and search.

## 📈 PromQL Queries

Useful queries for custom panels:

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
kubectl delete -f k8s/loki-stack.yaml
```

## 🎯 Best Practices

1. **Monitor What Matters**: Focus on metrics that indicate service health and ML model performance
2. **Set Meaningful Alerts**: Avoid alert fatigue by setting appropriate thresholds
3. **Regular Review**: Check dashboards regularly and adjust queries as needed
4. **Resource Limits**: Monitor Prometheus memory usage, increase limits if needed
5. **Data Retention**: Configure retention period based on your needs (default: 15 days)

