# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-10

### Added
- GitHub Container Registry (ghcr.io) integration for automated Docker image publishing
- Proper workflow permissions for packages and security events
- Enhanced test data with balanced classes for better stratified splitting

### Changed
- Updated `actions/upload-artifact` from deprecated v3 to v4
- Updated `github/codeql-action/upload-sarif` from deprecated v2 to v3
- Fixed unit tests to handle stratified splitting with proper sample sizes
- Updated data preprocessing to use `ffill()` instead of deprecated `fillna(method='ffill')`

### Fixed
- CI/CD workflow deprecation warnings resolved
- Security scan permissions error ("Resource not accessible by integration")
- Test failures in `test_split_train_test`, `test_scale_features`, and `test_preprocess_pipeline`
- Added coverage files (`.coverage`, `coverage.xml`, `htmlcov/`, `.pytest_cache/`) to `.gitignore`

## [1.0.0] - 2026-07-08

### Added
- Initial project release
- Data acquisition and preprocessing module
- Feature engineering pipeline
- Model training with Logistic Regression and Random Forest
- MLflow experiment tracking integration
- FastAPI REST API for model serving
- Comprehensive test suite with Pytest
- Docker containerization
- Kubernetes deployment manifests
- GitHub Actions CI/CD pipeline
- Prometheus and Grafana monitoring setup
- Complete documentation with architecture diagrams
- Quick start guide
- Model card documentation
- Contributing guidelines

### Features
- `/predict` endpoint for heart disease prediction
- `/health` endpoint for health checks
- `/model/info` endpoint for model metadata
- `/metrics` endpoint for Prometheus metrics
- Automated data preprocessing
- Model versioning with MLflow
- Cross-validation evaluation
- Comprehensive metrics (Accuracy, Precision, Recall, F1, ROC-AUC)

### Documentation
- README.md with Mermaid diagrams
- QUICKSTART.md for rapid setup
- MODEL_CARD.md for model documentation
- PROJECT_SUMMARY.md for completion status
- CONTRIBUTING.md for contribution guidelines
- Data download instructions

### DevOps
- GitHub Actions workflow for CI/CD
- Docker multi-stage build
- Kubernetes deployment with health checks
- docker-compose for local development
- Prometheus metrics integration
- Grafana dashboard configuration

### Testing
- Unit tests for data processing
- Unit tests for model training
- Integration tests for API
- Code coverage reporting
- Automated testing in CI/CD

### Deployment
- Local deployment instructions
- Docker deployment guide
- Kubernetes deployment guide
- Minikube deployment support
- Cloud deployment instructions (GKE/EKS/AKS)

---

## [Unreleased]

### Planned Features
- [ ] XGBoost model integration
- [ ] Feature importance visualization
- [ ] Data drift detection
- [ ] A/B testing framework
- [ ] Enhanced monitoring dashboards
- [ ] Automated model retraining
- [ ] Model explainability (SHAP/LIME)
- [ ] Batch prediction endpoint
- [ ] Model performance alerts

### Planned Improvements
- [ ] Optimize Docker image size
- [ ] Add request caching
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Enhance error messages
- [ ] Add input data validation
- [ ] Improve logging format
- [ ] Add more comprehensive tests

---

## Version History

### Version 1.0.0 (2026-07-08)
- **First stable release**
- Complete MLOps pipeline implementation
- Production-ready with all requirements met

---

## Breaking Changes

No breaking changes in version 1.0.0 (initial release)

---

## Migration Guide

N/A for version 1.0.0 (initial release)

---

## Acknowledgments

- BITS Pilani for the assignment requirements
- UCI Machine Learning Repository for the dataset
- FastAPI, MLflow, and other open-source communities

---

For detailed information about each version, please refer to the respective release notes.
