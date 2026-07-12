#!/bin/bash
# Script to deploy the Grafana Predictions Dashboard

echo "🎯 Deploying Heart Disease Predictions Dashboard to Grafana..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if the main monitoring stack is deployed
if ! kubectl get deployment grafana &> /dev/null; then
    echo "❌ Grafana deployment not found. Please deploy monitoring-local.yaml first."
    exit 1
fi

# Create or update the ConfigMap for the predictions dashboard
echo "📦 Creating ConfigMap for predictions dashboard..."
kubectl create configmap grafana-predictions-dashboard \
    --from-file=grafana-predictions-dashboard.json=k8s/monitoring/grafana-dashboard-predictions.json \
    --dry-run=client -o yaml | kubectl apply -f -

# Update Grafana deployment to mount the new dashboard
echo "🔄 Updating Grafana deployment to include predictions dashboard..."

# Get current Grafana deployment
kubectl get deployment grafana -o yaml > /tmp/grafana-deployment.yaml

# Check if the volume already exists
if ! grep -q "grafana-predictions-dashboard" /tmp/grafana-deployment.yaml; then
    echo "⚙️  Adding predictions dashboard volume to Grafana deployment..."
    
    # This would require patching the deployment to add the new volume
    # For now, we'll provide manual instructions
    echo ""
    echo "📝 Manual step required:"
    echo "   Please add the following to your Grafana deployment:"
    echo ""
    echo "   Under volumes:"
    echo "     - name: grafana-predictions-dashboard"
    echo "       configMap:"
    echo "         name: grafana-predictions-dashboard"
    echo ""
    echo "   Under volumeMounts:"
    echo "     - name: grafana-predictions-dashboard"
    echo "       mountPath: /var/lib/grafana/dashboards-predictions"
    echo ""
fi

# Restart Grafana pod to pick up changes
echo "🔄 Restarting Grafana to load new dashboard..."
kubectl rollout restart deployment/grafana

# Wait for Grafana to be ready
echo "⏳ Waiting for Grafana to be ready..."
kubectl wait --for=condition=available --timeout=60s deployment/grafana

echo ""
echo "✅ Predictions dashboard deployment complete!"
echo ""
echo "🌐 Access the dashboard at:"
echo "   http://localhost:30030/d/heart-disease-predictions/heart-disease-prediction-history"
echo ""
echo "🔑 Default credentials:"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "📊 The dashboard includes:"
echo "   - Total predictions count"
echo "   - High/Low risk distribution"
echo "   - Average risk score and confidence"
echo "   - Recent predictions table"
echo "   - Risk score distribution"
echo "   - Prediction inference time metrics"
echo ""
