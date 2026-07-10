# Kubernetes Deployment Configurations

This directory contains Kubernetes manifests for deploying the Heart Disease Prediction API.

## Files

### Deployment Configurations

- **`deployment-local.yaml`** - For local testing with Rancher Desktop, Minikube, or Docker Desktop Kubernetes
  - Uses NodePort service type
  - Single replica (resource efficient)
  - Lower resource limits
  - Access via: `http://localhost:30080`

- **`deployment-cloud.yaml`** - For cloud deployments (AWS EKS, Azure AKS, Google GKE)
  - Uses LoadBalancer service type
  - 2 replicas for high availability
  - Higher resource limits
  - External IP assigned by cloud provider

- **`deployment.yaml`** - Generic deployment (kept for backward compatibility)
  - Can be customized for specific needs

### Configuration Files

- **`configmap.yaml`** - Environment variables and application configuration

## Quick Start

### Local Deployment (Rancher Desktop / Minikube)

```bash
# Verify kubectl is configured
kubectl cluster-info

# Apply ConfigMap (optional)
kubectl apply -f k8s/configmap.yaml

# Deploy application
kubectl apply -f k8s/deployment-local.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Access the API
# Open browser: http://localhost:30080
# Or test with curl:
curl http://localhost:30080/health
```

### Cloud Deployment (AWS/Azure/GCP)

```bash
# Apply ConfigMap (optional)
kubectl apply -f k8s/configmap.yaml

# Deploy application
kubectl apply -f k8s/deployment-cloud.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Wait for external IP (may take 1-2 minutes)
kubectl get service heart-disease-api-service -w

# Once EXTERNAL-IP is assigned, access via:
# http://<EXTERNAL-IP>/health
```

## Testing the Deployment

### Health Check
```bash
# Local
curl http://localhost:30080/health

# Cloud
curl http://<EXTERNAL-IP>/health
```

### Make Prediction
```bash
# Local
curl -X POST http://localhost:30080/predict \
  -H "Content-Type: application/json" \
  -d @../test_data.json

# Cloud
curl -X POST http://<EXTERNAL-IP>/predict \
  -H "Content-Type: application/json" \
  -d @../test_data.json
```

### Access API Documentation
- Local: http://localhost:30080/docs
- Cloud: http://<EXTERNAL-IP>/docs

## Monitoring

### Deploy Monitoring Stack

Deploy Prometheus and Grafana for metrics visualization:

```bash
# Deploy monitoring stack
kubectl apply -f k8s/monitoring-local.yaml

# Check status
kubectl get pods -l app=prometheus
kubectl get pods -l app=grafana

# View services
kubectl get svc prometheus grafana
```

### Access Monitoring Dashboards

- **Prometheus UI**: http://localhost:30090
- **Grafana Dashboard**: http://localhost:30030 (admin/admin)
- **API Metrics Endpoint**: http://localhost:30080/metrics

**First Time Grafana Setup:**
1. Open http://localhost:30030
2. Login with admin/admin
3. Add Prometheus data source: `http://prometheus:9090`
4. Create dashboards using PromQL queries

See [monitoring/README.md](../monitoring/README.md) for detailed setup and dashboard examples.

### View Logs
```bash
# Get pod name
kubectl get pods

# View logs
kubectl logs <pod-name>

# Follow logs
kubectl logs -f <pod-name>
```

### Check Pod Status
```bash
kubectl describe pod <pod-name>
```

### Port Forwarding (Alternative to NodePort)
```bash
# Forward local port 8080 to pod port 8000
kubectl port-forward service/heart-disease-api-service 8080:80

# Access via: http://localhost:8080
```

## Updating the Deployment

### Update Image
```bash
# Update to specific tag
kubectl set image deployment/heart-disease-api api=ghcr.io/2024ac05841-design/heart-health-classifier:v1.1.0

# Rollout status
kubectl rollout status deployment/heart-disease-api

# Rollback if needed
kubectl rollout undo deployment/heart-disease-api
```

### Scale Replicas
```bash
# Scale to 3 replicas
kubectl scale deployment heart-disease-api --replicas=3
```

## Cleanup

```bash
# Delete deployment and service
kubectl delete -f k8s/deployment-local.yaml
# or
kubectl delete -f k8s/deployment-cloud.yaml

# Delete ConfigMap (if applied)
kubectl delete -f k8s/configmap.yaml
```

## Troubleshooting

### Pod not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### ImagePullBackOff error
If the image is in a private registry (ghcr.io with private repo):
```bash
# Create image pull secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-token> \
  --docker-email=<email>

# Add to deployment spec:
# spec:
#   imagePullSecrets:
#   - name: ghcr-secret
```

### Service not accessible
- **Local**: Ensure NodePort 30080 is not blocked by firewall
- **Cloud**: Wait for LoadBalancer provisioning (1-2 minutes)

## Environment-Specific Notes

### Rancher Desktop
- Kubernetes is built-in, no extra setup needed
- NodePort 30080 accessible directly via localhost
- Uses containerd or dockerd as container runtime

### Minikube
- May need to run `minikube service heart-disease-api-service` to access NodePort
- Or use `minikube tunnel` for LoadBalancer simulation

### Docker Desktop
- Kubernetes optional, must be enabled in settings
- NodePort accessible via localhost

### AWS EKS / Azure AKS / Google GKE
- LoadBalancer automatically provisions cloud load balancer
- May incur additional costs for load balancer
- External IP assigned automatically
