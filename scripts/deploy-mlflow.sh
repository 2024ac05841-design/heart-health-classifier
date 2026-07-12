#!/bin/bash
set -e

echo ""
echo "================================================================"
echo "    🔬 MLflow Kubernetes Deployment"
echo "================================================================"
echo ""

# Check if mlruns_training exists
if [ ! -d "mlruns_training" ]; then
    echo "❌ Error: mlruns_training/ directory not found"
    echo "   Run training first: python scripts/train_model.py"
    exit 1
fi

echo "📋 Step 1: Deploying MLflow to Kubernetes..."
kubectl apply -f k8s/mlflow.yaml

echo ""
echo "⏳ Step 2: Waiting for MLflow pod to be ready..."
sleep 5

# Wait for pod to be running
timeout=60
elapsed=0
while [ $elapsed -lt $timeout ]; do
    pod_status=$(kubectl get pods -l app=mlflow -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "")
    if [ "$pod_status" = "Running" ]; then
        echo "   ✓ MLflow pod is running"
        break
    fi
    echo "   Waiting for pod... (${elapsed}s/${timeout}s)"
    sleep 5
    elapsed=$((elapsed + 5))
done

if [ $elapsed -ge $timeout ]; then
    echo ""
    echo "⚠ Warning: Pod may still be starting. Check with: kubectl get pods -l app=mlflow"
    echo ""
    echo "Continuing with data sync..."
else
    # Wait a bit more for the init container to complete
    sleep 5
fi

echo ""
echo "📤 Step 3: Uploading local experiment data to MLflow pod..."

# Get the pod name
pod_name=$(kubectl get pods -l app=mlflow -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -z "$pod_name" ]; then
    echo ""
    echo "❌ Error: Could not find MLflow pod"
    echo "   Check deployment status: kubectl get pods -l app=mlflow"
    exit 1
fi

echo "   Pod name: $pod_name"

# Create a tar archive of mlruns_training
echo ""
echo "   Creating archive of experiment data..."
temp_archive="mlruns_training.tar"
if [ -f "$temp_archive" ]; then
    rm -f "$temp_archive"
fi

tar -cf "$temp_archive" mlruns_training/

echo "   ✓ Archive created: $temp_archive"

# Copy archive to pod
echo ""
echo "   Copying data to MLflow pod..."
kubectl cp "$temp_archive" "default/${pod_name}:/tmp/mlruns_training.tar"

# Extract in pod
echo "   Extracting data in pod..."
kubectl exec -it "$pod_name" -- sh -c "cd /mlflow && tar -xf /tmp/mlruns_training.tar && rm /tmp/mlruns_training.tar"

# Clean up local archive
rm -f "$temp_archive"
echo "   ✓ Experiment data uploaded successfully!"

echo ""
echo "✅ Step 4: MLflow UI is ready!"
echo ""
echo "================================================================"
echo "    🎯 ACCESS MLFLOW UI"
echo "================================================================"
echo ""
echo "📱 External Access:"
echo "   http://localhost:30050"
echo ""
echo "📊 What You Can View:"
echo "   ✓ All training runs and experiments"
echo "   ✓ Parameters (model_type, n_estimators, test_size, random_state)"
echo "   ✓ Metrics (accuracy, precision, recall, f1, roc_auc)"
echo "   ✓ Model artifacts (sklearn models, conda env, requirements)"
echo "   ✓ Compare multiple runs side-by-side"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:    kubectl logs -f deployment/mlflow"
echo "   Check status: kubectl get pods -l app=mlflow"
echo "   Port forward: kubectl port-forward svc/mlflow-service 5000:5000"
echo "   Delete:       kubectl delete -f k8s/mlflow.yaml"
echo ""
echo "================================================================"
echo ""

# Try to open in browser (macOS/Linux)
echo "🌐 Opening MLflow UI in browser..."
sleep 3

if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:30050"  # Linux
elif command -v open > /dev/null; then
    open "http://localhost:30050"  # macOS
else
    echo "Please open http://localhost:30050 in your browser"
fi
