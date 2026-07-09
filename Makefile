# Makefile for Heart Disease MLOps Project

.PHONY: help install train test clean docker k8s

# Default target
.DEFAULT_GOAL := help

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Heart Disease MLOps - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install Python dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	pip install --upgrade pip
	pip install -r requirements.txt

download-data: ## Download dataset
	@echo "$(GREEN)Downloading dataset...$(NC)"
	python data/download_data.py

train: ## Train models
	@echo "$(GREEN)Training models...$(NC)"
	python scripts/train_model.py

mlflow: ## Start MLflow UI
	@echo "$(GREEN)Starting MLflow UI on http://localhost:5000$(NC)"
	mlflow ui --port 5000

run-api: ## Run API locally
	@echo "$(GREEN)Starting API on http://localhost:8000$(NC)"
	uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests/ -v

test-coverage: ## Run tests with coverage
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	pytest tests/ --cov=src --cov=api --cov-report=html --cov-report=term
	@echo "$(GREEN)Coverage report: htmlcov/index.html$(NC)"

lint: ## Run code linters
	@echo "$(GREEN)Running linters...$(NC)"
	flake8 src/ api/ --count --statistics
	black --check src/ api/

format: ## Format code with black
	@echo "$(GREEN)Formatting code...$(NC)"
	black src/ api/

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t heart-disease-api:latest .

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest
	@echo "$(GREEN)API running at http://localhost:8000$(NC)"

docker-stop: ## Stop Docker container
	@echo "$(GREEN)Stopping Docker container...$(NC)"
	docker stop heart-api || true
	docker rm heart-api || true

docker-logs: ## View Docker container logs
	docker logs -f heart-api

docker-compose-up: ## Start all services with docker-compose
	@echo "$(GREEN)Starting all services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)API: http://localhost:8000$(NC)"
	@echo "$(GREEN)Prometheus: http://localhost:9090$(NC)"
	@echo "$(GREEN)Grafana: http://localhost:3000 (admin/admin)$(NC)"

docker-compose-down: ## Stop all services
	@echo "$(GREEN)Stopping all services...$(NC)"
	docker-compose down

k8s-deploy: ## Deploy to Kubernetes
	@echo "$(GREEN)Deploying to Kubernetes...$(NC)"
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml

k8s-delete: ## Delete Kubernetes deployment
	@echo "$(GREEN)Deleting Kubernetes deployment...$(NC)"
	kubectl delete -f k8s/deployment.yaml
	kubectl delete -f k8s/configmap.yaml

k8s-status: ## Check Kubernetes deployment status
	@echo "$(GREEN)Checking deployment status...$(NC)"
	kubectl get pods
	kubectl get services
	kubectl get deployments

k8s-logs: ## View Kubernetes logs
	kubectl logs -l app=heart-disease-api -f

clean: ## Clean up generated files
	@echo "$(GREEN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-all: clean ## Clean everything including models and data
	@echo "$(RED)Warning: This will delete models and processed data!$(NC)"
	rm -rf models/*.pkl models/*.json 2>/dev/null || true
	rm -rf mlruns_training/ mlartifacts/ 2>/dev/null || true
	@echo "$(GREEN)Deep cleanup complete!$(NC)"

setup: install download-data ## Initial setup (install + download data)
	@echo "$(GREEN)Setup complete!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. make train    - Train models"
	@echo "  2. make run-api  - Start API"
	@echo "  3. make test     - Run tests"

all: setup train test ## Run complete pipeline
	@echo "$(GREEN)All tasks completed!$(NC)"
