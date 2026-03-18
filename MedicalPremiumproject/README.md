# 🏥 Medical Insurance Premium Predictor

A Streamlit web application that predicts annual medical insurance premiums based on patient health profiles using a Random Forest machine learning model.

## Features

- 📊 Interactive web interface for entering patient health data
- 🤖 Machine learning-powered predictions using Random Forest
- 💡 Real-time premium estimates
- 📈 BMI calculation and health warnings
- 🎯 Easy-to-use sliders and dropdowns

## How to Use

1. Enter patient details in the sidebar:
   - Age, Height, Weight
   - Medical conditions (Diabetes, Blood Pressure, etc.)
   - Medical history (Transplants, Surgeries, etc.)

2. Click "Calculate Premium" to get the predicted annual insurance premium

## Live Demo

🚀 [Try the app here](https://your-app-url.streamlit.app) _(Update this after deployment)_

## Local Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: Age, BMI, Diabetes, Blood Pressure Problems, Transplants, Chronic Diseases, Allergies, Cancer Family History, Major Surgeries
- **Output**: Annual Insurance Premium (USD)

## Files

- `app.py` - Main Streamlit application
- `medical_premium_model.pkl` - Trained Random Forest model
- `model_columns.pkl` - Feature column names
- `Medicalpremium.csv` - Dataset used for training
- `Insurance.ipynb` - Jupyter notebook with model training

## Technologies Used

- Python 3.14
- Streamlit
- Pandas
- Scikit-learn
- Joblib


