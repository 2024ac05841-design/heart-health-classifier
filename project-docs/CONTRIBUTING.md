# Contributing to Heart Disease MLOps Project

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Follow professional communication standards
- Focus on constructive feedback

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue template
3. Provide detailed information:
   - Environment details
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Open an issue with "Feature Request" label
2. Describe the feature clearly
3. Explain the use case
4. Provide examples if possible

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Follow coding standards
   - Add tests for new features
   - Update documentation

4. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

5. **Run linting:**
   ```bash
   flake8 src/ api/
   black src/ api/
   ```

6. **Commit your changes:**
   ```bash
   git commit -m "feat: add your feature description"
   ```

7. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use Black for formatting
- Maximum line length: 127 characters
- Use type hints where appropriate

### Naming Conventions

- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update README.md for new features
- Add inline comments for complex logic

### Testing

- Write unit tests for all new code
- Aim for >80% code coverage
- Use descriptive test names
- Include both positive and negative tests

## Project Structure

```
src/           - Core ML logic
api/           - API implementation
tests/         - Test files
scripts/       - Training and utility scripts
k8s/           - Kubernetes configs
monitoring/    - Monitoring configs
```

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/2024ac05841-design/heart-disease-mlops.git
   cd heart-disease-mlops
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

## Commit Message Guidelines

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

Examples:
- `feat: add gradient boosting model`
- `fix: resolve API timeout issue`
- `docs: update deployment guide`

## Areas for Contribution

### High Priority

- [ ] Improve model performance with hyperparameter tuning
- [ ] Add more ML algorithms (XGBoost, LightGBM)
- [ ] Implement feature importance visualization
- [ ] Add data drift detection
- [ ] Enhance monitoring dashboards

### Medium Priority

- [ ] Add more comprehensive tests
- [ ] Improve error handling
- [ ] Add request validation
- [ ] Implement caching
- [ ] Add rate limiting

### Documentation

- [ ] Add more examples
- [ ] Create video tutorials
- [ ] Improve API documentation
- [ ] Add troubleshooting guide

## Review Process

1. All PRs require review before merging
2. CI/CD pipeline must pass
3. Tests must pass with >80% coverage
4. Code must be formatted with Black
5. Documentation must be updated

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
