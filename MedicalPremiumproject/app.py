import streamlit as st
import pandas as pd
import joblib
import os

# 1. Page Config MUST be first Streamlit command
st.set_page_config(page_title="Medical Insurance Premium Calculator", page_icon="🏥", layout="wide")

# 2. Load the saved model and column names
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

# 3. Session state to remember last prediction
if "prediction" not in st.session_state:
    st.session_state.prediction = None

# 4. Responsive CSS
st.markdown("""
    <style>
        .block-container {
            max-width: 100%;
            padding: 1rem 0.75rem 1.5rem !important;
        }
        .app-title {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            font-weight: 700;
            line-height: 1.2;
            margin: 0.5rem 0;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .app-subtitle {
            font-size: clamp(0.95rem, 3.5vw, 1.05rem);
            margin-bottom: 0.5rem;
        }
        /* Prevent input widgets from overflowing */
        .stNumberInput,
        .stSelectbox,
        .stSlider {
            width: 100% !important;
        }
        .premium-box {
            background: linear-gradient(135deg, #1a472a, #2d6a4f);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-size: clamp(1rem, 3.5vw, 1.8rem);
            font-weight: bold;
            margin-top: 1rem;
            word-break: break-word;
        }
        @media (min-width: 769px) {
            .block-container {
                padding: 1.5rem 2rem 2rem 2rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">🏥 Medical Insurance Premium Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Fill in your health details below to get an instant premium estimate.</div>', unsafe_allow_html=True)
st.divider()

# 5. Input Fields in a form
with st.form("premium_form"):
    # Always use single column layout - simpler and mobile-friendly
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

    # 6. Auto BMI
    bmi = weight / ((height / 100) ** 2)
    st.metric("Your Calculated BMI", f"{bmi:.1f}")

    submit_prediction = st.form_submit_button("💰 Predict My Premium", use_container_width=True)

# 7. Predict Button
if submit_prediction:
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
