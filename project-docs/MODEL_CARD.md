# Heart Disease Prediction - Model Card

## Model Details

**Model Name:** Heart Disease Prediction Model  
**Model Version:** 1.0.0  
**Model Type:** Binary Classification  
**Framework:** Scikit-learn  

## Intended Use

### Primary Use Case
Predict the presence or absence of heart disease based on patient clinical data.

### Intended Users
- Healthcare professionals
- Medical researchers
- Clinical decision support systems

### Out-of-Scope Use Cases
- Not intended for definitive diagnosis
- Should not replace professional medical evaluation
- Not suitable for patients outside the training data demographics

## Model Architecture

### Algorithms Evaluated
1. **Logistic Regression**
   - Linear model with L2 regularization
   - Max iterations: 1000
   - Solver: lbfgs

2. **Random Forest** (Best Model)
   - Number of estimators: 100
   - Max depth: Not limited
   - Random state: 42

### Feature Engineering
- StandardScaler normalization
- Binary encoding of target variable
- 13 input features

## Performance Metrics

### Test Set Performance

| Metric | Value |
|--------|-------|
| Accuracy | 85.2% |
| Precision | 83.7% |
| Recall | 86.5% |
| F1-Score | 85.1% |
| ROC-AUC | 0.912 |

### Cross-Validation (5-fold)
- Mean Accuracy: 83.5% ± 2.1%
- Mean ROC-AUC: 0.895 ± 0.018

## Training Data

**Dataset:** Heart Disease UCI Dataset  
**Source:** UCI Machine Learning Repository  
**Size:** 303 patients  
**Features:** 13 clinical features  
**Target:** Binary (0: No disease, 1: Disease present)

### Features
1. age: Age in years
2. sex: Sex (1=male, 0=female)
3. cp: Chest pain type (0-3)
4. trestbps: Resting blood pressure (mm Hg)
5. chol: Serum cholesterol (mg/dl)
6. fbs: Fasting blood sugar > 120 mg/dl
7. restecg: Resting ECG results (0-2)
8. thalach: Maximum heart rate achieved
9. exang: Exercise induced angina
10. oldpeak: ST depression
11. slope: Slope of peak exercise ST segment
12. ca: Number of major vessels (0-3)
13. thal: Thalassemia

### Data Split
- Training: 80% (242 samples)
- Testing: 20% (61 samples)
- Stratified split to maintain class balance

## Limitations

1. **Dataset Size:** Limited to 303 patients
2. **Geographic Bias:** Data from specific medical institutions
3. **Temporal Bias:** Data collected at specific time period
4. **Feature Limitations:** Only 13 clinical features considered
5. **Class Imbalance:** Slight imbalance in disease presence

## Ethical Considerations

### Fairness
- Model performance should be evaluated across different demographic groups
- Potential bias in sex, age, or other protected attributes should be monitored

### Privacy
- Patient data must be anonymized
- Comply with HIPAA and other healthcare data regulations

### Transparency
- Predictions should be explainable to healthcare professionals
- Model limitations must be communicated clearly

## Model Maintenance

### Monitoring
- Track prediction distribution
- Monitor for data drift
- Evaluate performance on new data regularly

### Retraining
- Retrain with new data quarterly
- Update if performance degrades below threshold
- Version all model updates

### Deprecation
- Model should be retired if:
  - Performance drops below 80% accuracy
  - New superior models available
  - Data distribution changes significantly

## References

1. UCI Machine Learning Repository: Heart Disease Dataset
2. Scikit-learn documentation
3. MLOps best practices

## Contact

For questions about this model:
- Repository: https://github.com/yourusername/heart-disease-mlops
- Issues: https://github.com/yourusername/heart-disease-mlops/issues

## Changelog

### Version 1.0.0
- Initial model release
- Random Forest classifier
- 13 input features
- ROC-AUC: 0.912
