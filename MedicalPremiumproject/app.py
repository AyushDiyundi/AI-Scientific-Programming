import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# 1. Load the saved model and column names
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'medical_premium_model.pkl'))
model_columns = joblib.load(os.path.join(BASE_DIR, 'model_columns.pkl'))

# 2. Session state to remember last prediction
if "prediction" not in st.session_state:
    st.session_state.prediction = None

# 3. Page Config
st.set_page_config(page_title="Medical Insurance Premium Calculator", page_icon="🏥", layout="wide")

# 4. Responsive CSS
st.markdown("""
    <style>
        .block-container {
            padding: 1.5rem 2rem 2rem 2rem;
            max-width: 100%;
        }
        h1 {
            font-size: clamp(1.4rem, 4vw, 2.2rem) !important;
        }
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
        @media (max-width: 640px) {
            .block-container {
                padding: 0.75rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Medical Insurance Premium Calculator")
st.write("Fill in your health details below to get an instant premium estimate.")
st.divider()

# 5. Input Fields in two columns
col1, col2 = st.columns(2)

with col1:
    age        = st.slider("Age", 18, 66, 30)
    height     = st.number_input("Height (cm)", 140, 200, 165)
    weight     = st.number_input("Weight (kg)", 40, 150, 70)
    diabetes   = st.selectbox("Diabetes?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    bp         = st.selectbox("Blood Pressure Problems?", [0, 1], format_func=lambda x: "Yes" if x else "No")

with col2:
    transplant = st.selectbox("Any Transplants?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    chronic    = st.selectbox("Any Chronic Diseases?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    allergies  = st.selectbox("Known Allergies?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    cancer_fam = st.selectbox("History of Cancer in Family?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    surgeries  = st.slider("Number of Major Surgeries", 0, 3, 0)

st.divider()

# 6. Auto BMI
bmi = weight / ((height / 100) ** 2)
st.metric("Your Calculated BMI", f"{bmi:.1f}")

# 7. Predict Button
if st.button("💰 Predict My Premium", use_container_width=True):
    input_data = pd.DataFrame(
        [[age, diabetes, bp, transplant, chronic,
          height, weight, allergies, cancer_fam, surgeries, round(bmi, 2)]],
        columns=model_columns
    )
    st.session_state.prediction = model.predict(input_data)[0]

# 8. Show result (persists even if user changes a slider)
if st.session_state.prediction is not None:
    st.markdown(
        f'<div class="premium-box">Estimated Annual Premium: ₹{st.session_state.prediction:,.0f}</div>',
        unsafe_allow_html=True
    )
    if bmi > 30:
        st.warning("⚠️ Note: High BMI is a significant risk factor in this premium calculation.")
