import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# 1. Load the saved model and column names
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'medical_premium_model.pkl'))
model_columns = joblib.load(os.path.join(BASE_DIR, 'model_columns.pkl'))

# 2. Setup the Web Page UI
st.set_page_config(page_title="Insurance Predictor", page_icon="🏥", layout="wide")

# Responsive CSS
st.markdown("""
    <style>
        /* Fluid container */
        .block-container {
            padding: 1rem 1rem 2rem 1rem;
            max-width: 100%;
        }
        /* Responsive title */
        h1 {
            font-size: clamp(1.4rem, 4vw, 2.2rem) !important;
        }
        h2, h3 {
            font-size: clamp(1rem, 3vw, 1.5rem) !important;
        }
        /* Prediction result box */
        .premium-box {
            background: linear-gradient(135deg, #1a472a, #2d6a4f);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            font-size: clamp(1.2rem, 3.5vw, 2rem);
            font-weight: bold;
            margin-top: 1rem;
            word-break: break-word;
        }
        /* Sidebar responsive */
        [data-testid="stSidebar"] {
            min-width: 220px;
            max-width: 320px;
        }
        /* Make dataframe fill width */
        .stDataFrame {
            width: 100% !important;
        }
        /* Stack columns on small screens */
        @media (max-width: 640px) {
            [data-testid="stSidebar"] {
                min-width: 100%;
                max-width: 100%;
            }
            .block-container {
                padding: 0.5rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Medical Insurance Premium Predictor")
st.markdown("""
Enter the patient's health details in the sidebar to get an instant **Annual Premium Estimate (₹)**.  
This model uses Random Forest logic to analyze health risks.
""")

# 3. Create Input Fields
st.sidebar.header("User Health Profile")


def user_input_features():
    age = st.sidebar.slider("Age", 18, 100, 30)
    height = st.sidebar.number_input("Height (cm)", 120, 220, 170)
    weight = st.sidebar.number_input("Weight (kg)", 30, 200, 70)

    # Binary Inputs (Yes/No)
    diabetes = st.sidebar.selectbox("Diabetes", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    bp = st.sidebar.selectbox("Blood Pressure Problems", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    transplants = st.sidebar.selectbox("Any Transplants", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    chronic = st.sidebar.selectbox("Any Chronic Diseases", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    allergies = st.sidebar.selectbox("Known Allergies", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    cancer = st.sidebar.selectbox("Family History of Cancer", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    surgeries = st.sidebar.slider("Number of Major Surgeries", 0, 3, 0)

    # Calculate BMI automatically
    bmi = round(weight / ((height / 100) ** 2), 2)

    data = {
        'Age': age,
        'Diabetes': diabetes,
        'BloodPressureProblems': bp,
        'AnyTransplants': transplants,
        'AnyChronicDiseases': chronic,
        'Height': height,
        'Weight': weight,
        'KnownAllergies': allergies,
        'HistoryOfCancerInFamily': cancer,
        'NumberOfMajorSurgeries': surgeries,
        'BMI': bmi
    }
    return pd.DataFrame(data, index=[0])


# Get the inputs
input_df = user_input_features()

# 4. Display the inputs to the user
st.subheader("Patient Summary")
st.dataframe(input_df, use_container_width=True)

# 5. The Prediction Logic
if st.button("💰 Calculate Premium", use_container_width=True):
    # Ensure columns are in the exact order the model expects
    input_df = input_df[model_columns]

    prediction = model.predict(input_df)
    premium_inr = prediction[0]

    st.markdown(
        f'<div class="premium-box">Predicted Annual Premium: ₹{premium_inr:,.2f}</div>',
        unsafe_allow_html=True
    )

    # Add a health warning for high BMI
    if input_df['BMI'][0] > 30:
        st.warning("⚠️ Note: High BMI is a significant risk factor in this premium calculation.")
