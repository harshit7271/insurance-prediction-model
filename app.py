import streamlit as st
import requests
from datetime import datetime

# Custom CSS styling
def local_css():
    st.markdown(
        """
        <style>
        .main-container {
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
            padding: 2rem;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 8px 16px rgba(0,0,0,0.25);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1 {
            text-align: center;
            color: #003366;
            font-weight: bold;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #004080;
            font-size: 1.3rem;
            margin-bottom: 2rem;
            font-style: italic;
        }
        label {
            font-weight: 600;
            color: #002244;
            margin-top: 1rem;
            display: block;
        }
        .stButton > button {
            background-color: #0077cc;
            color: white;
            border-radius: 8px;
            height: 3rem;
            font-size: 1.1rem;
            border: none;
            transition: background-color 0.3s ease;
            width: 100%;
            margin-top: 1.5rem;
        }
        .stButton > button:hover {
            background-color: #005fa3;
            cursor: pointer;
        }
        .result {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            font-size: 1.2rem;
            color: #003366;
            line-height: 1.5;
        }
        .key-label {
            font-weight: 700;
            color: #004080;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


local_css()

# Sidebar 
st.sidebar.title("User Feedback")
user_name = st.sidebar.text_input("Name")
rating = st.sidebar.slider("Rate this app", 0, 5, 3)
st.sidebar.success(f"Hey {user_name}, you have rated our app {rating}")
comments = st.sidebar.text_area("Additional comments")

if st.sidebar.button("Submit Feedback"):
    if user_name.strip() == "" or comments.strip() == "":
        st.sidebar.error("Please provide your name and comments to submit feedback.")
    else:
        st.sidebar.success(f"Thanks for your feedback, {user_name}!")

# Main container for prediction
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("<h1>Insurance Premium Predictor</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your details below and get your premium estimate</p>', unsafe_allow_html=True)

with st.form("prediction_form"):
    age = st.number_input("Age", min_value=0, max_value=120)
    is_female = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Female" if x == 1 else "Male")
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)
    children = st.number_input("Number of children", min_value=0, max_value=10)
    is_smoker = st.selectbox("Smoker", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    region_southeast = st.selectbox("Region Southeast", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    bmi_category_Obese = st.selectbox("BMI Category Obese", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    submitted = st.form_submit_button("Predict Premium")

if submitted:
    if age == 0 or bmi == 0.0:
        st.error("Please enter valid Age and BMI values.")
    else:
        payload = {
            "age": age,
            "is_female": is_female,
            "bmi": bmi,
            "children": children,
            "is_smoker": is_smoker,
            "region_southeast": region_southeast,
            "bmi_category_Obese": bmi_category_Obese
        }
        try:
            response = requests.post("http://localhost:8000/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.markdown('<div class="result">', unsafe_allow_html=True)
                st.markdown(f'<p><span class="key-label">Predicted Premium:</span> ${result["predicted_premium"]:.2f}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><span class="key-label">Risk Category:</span> {result.get("risk_category", "N/A")}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><span class="key-label">Discount Eligibility:</span> {result.get("discount_eligibility", "N/A")}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><span class="key-label">Comparison to Average:</span> {result.get("comparison_to_average", "N/A")}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><span class="key-label">Model Version:</span> {result.get("model_version", "N/A")}</p>', unsafe_allow_html=True)
                timestamp = result.get('timestamp', datetime.utcnow().isoformat() + 'Z')
                st.markdown(f'<p><span class="key-label">Prediction Time (UTC):</span> {timestamp}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"API error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)


