# 📊 Monitoring Stack

This directory contains monitoring configurations for the Heart Disease Prediction API using Prometheus and Grafana.

## 🚀 Quick Start

### Deploy Monitoring Stack on Kubernetes

```bash
# Deploy Prometheus and Grafana
kubectl apply -f k8s/monitoring-local.yaml

# Check deployment status
kubectl get pods -l app=prometheus
kubectl get pods -l app=grafana

# View services
kubectl get svc prometheus
kubectl get svc grafana
```

### Access Dashboards

Once deployed, access the monitoring dashboards:

- **Prometheus UI**: http://localhost:30090
- **Grafana Dashboard**: http://localhost:30030
  - Username: `admin`
  - Password: `admin`

## 📈 Setting Up Grafana

### 1. Add Prometheus Data Source

1. Open Grafana at http://localhost:30030
2. Log in with `admin/admin`
3. Go to **Configuration** → **Data Sources**
4. Click **Add data source**
5. Select **Prometheus**
6. Set URL to: `http://prometheus:9090`
7. Click **Save & Test**

### 2. Create Dashboard

Import a pre-built dashboard or create custom panels:

#### Key Metrics to Track

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
