# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -l app=heart-disease-api

# Get service URL (for Minikube)
minikube service heart-disease-api-service --url

# Delete deployment
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/configmap.yaml
