# Data Download Instructions

## Option 1: Automatic Download (Recommended)

Try the automatic download script first:

```bash
python data/download_data.py
```

If you encounter SSL certificate errors, proceed to Option 2.

## Option 2: Manual Download

### Step 1: Visit UCI Repository

Go to: https://archive.ics.uci.edu/ml/datasets/Heart+Disease

### Step 2: Download the Dataset

Download `processed.cleveland.data` from the repository.

### Step 3: Save to Project

Save the file to: `data/raw/heart_disease.csv`

### Step 4: Format the Data

The data should have these columns:
- age
- sex
- cp
- trestbps
- chol
- fbs
- restecg
- thalach
- exang
- oldpeak
- slope
- ca
- thal
- target

## Option 3: Use Sample Data (For Testing)

For quick testing and development, use the sample data generator:

```bash
python data/create_sample_data.py
```

⚠️ **Note:** Sample data is synthetic and for demonstration only. Use real data for production.

## Troubleshooting

### SSL Certificate Error

If you get SSL certificate errors:

1. **Windows:**
   ```powershell
   # Install certificates
   pip install --upgrade certifi
   ```

2. **Python SSL Context:**
   ```python
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   ```

### Connection Timeout

If the download times out:
- Check your internet connection
- Try manual download (Option 2)
- Use sample data for initial testing (Option 3)

## Data Source

**Dataset:** Heart Disease UCI Dataset  
**URL:** https://archive.ics.uci.edu/ml/datasets/Heart+Disease  
**Citation:**
```
Janosi,Andras, Steinbrunn,William, Pfisterer,Matthias, and Detrano,Robert. (1988). 
Heart Disease. UCI Machine Learning Repository. https://doi.org/10.24432/C52P4X.
```

## Next Steps

After obtaining the data:

1. Explore the data using Python:
   ```powershell
   python -c "from src.data_processing import load_and_clean_data; df = load_and_clean_data('data/raw/heart_disease.csv'); print(df.describe()); print(df.info())"
   ```

2. Train models:
   ```bash
   python scripts/train_model.py
   ```
