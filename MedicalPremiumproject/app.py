import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Medical Insurance Premium Calculator", page_icon="🏥", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    model = joblib.load(os.path.join(BASE_DIR, 'medical_premium_model.pkl'))
    model_columns = joblib.load(os.path.join(BASE_DIR, 'model_columns.pkl'))
    return model, model_columns

try:
    model, model_columns = load_model()
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

if "prediction" not in st.session_state:
    st.session_state.prediction = None
st.markdown("""
    <style>
        header {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            display: none !important;
        }
        .stAppToolbar {
            display: none !important;
        }
        
        .block-container {
            max-width: 100%;
            padding: 1.5rem 0.85rem 8rem !important;
        }
        
        .app-title {
            font-size: clamp(1.8rem, 6vw, 2.8rem);
            font-weight: 700;
            line-height: 1.35;
            margin: 0 0 0.75rem 0;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: normal;
        }
        
        .app-subtitle {
            font-size: clamp(0.9rem, 3.2vw, 1.05rem);
            margin-bottom: 1.5rem;
            line-height: 1.5;
            color: #b0bec5;
        }
        
        .stForm {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }
        
        .stDivider {
            margin: 1.5rem 0 !important;
        }
        
        .stNumberInput,
        .stSelectbox,
        .stSlider {
            width: 100% !important;
        }
        
        .stMetric {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 1.25rem;
            border-radius: 8px;
            margin: 1.5rem 0;
        }
        
        .premium-box {
            background: linear-gradient(135deg, #1a472a, #2d6a4f);
            color: white;
            padding: 1.5rem 1.25rem;
            border-radius: 12px;
            text-align: center;
            font-size: clamp(1.1rem, 4vw, 2rem);
            font-weight: bold;
            margin-top: 2rem;
            margin-bottom: 6rem;
            word-break: break-word;
            line-height: 1.4;
            box-shadow: 0 4px 12px rgba(26, 71, 42, 0.3);
        }
        
        @media (min-width: 769px) {
            .block-container {
                padding: 2rem 2.5rem 6rem 2.5rem !important;
            }
            .app-title {
                font-size: 2.8rem;
                margin-bottom: 0.75rem;
            }
            .app-subtitle {
                font-size: 1.05rem;
                margin-bottom: 2rem;
            }
            .premium-box {
                margin-bottom: 4rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">🏥 Medical Insurance Premium Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Fill in your health details below to get an instant premium estimate.</div>', unsafe_allow_html=True)
st.divider()

with st.form("premium_form"):
    age = st.slider("Age", 18, 66, 30)
    height = st.number_input("Height (cm)", min_value=140, max_value=200, value=165, step=1)
    weight = st.number_input("Weight (kg)", min_value=40, max_value=150, value=70, step=1)
    diabetes = st.selectbox("Diabetes?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    bp = st.selectbox("Blood Pressure Problems?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    transplant = st.selectbox("Any Transplants?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    chronic = st.selectbox("Any Chronic Diseases?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    allergies = st.selectbox("Known Allergies?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    cancer_fam = st.selectbox("Family Cancer History?", [0, 1], format_func=lambda x: "Yes" if x else "No")
    surgeries = st.slider("Major Surgeries", 0, 3, 0)

    st.divider()

    bmi = weight / ((height / 100) ** 2)
    st.metric("Your Calculated BMI", f"{bmi:.1f}")

    submit_prediction = st.form_submit_button("💰 Predict My Premium", use_container_width=True)

if submit_prediction:
    input_data = pd.DataFrame(
        [[age, diabetes, bp, transplant, chronic,
          height, weight, allergies, cancer_fam, surgeries, round(bmi, 2)]],
        columns=model_columns
    )
    st.session_state.prediction = model.predict(input_data)[0]

if st.session_state.prediction is not None:
    st.markdown(
        f'<div class="premium-box">Estimated Annual Premium: ₹{st.session_state.prediction:,.0f}</div>',
        unsafe_allow_html=True
    )
    if bmi > 30:
        st.warning("⚠️ Note: High BMI is a significant risk factor in this premium calculation.")
