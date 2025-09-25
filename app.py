import streamlit as st
import requests

# Custom CSS for styling
custom_css = """
<style>
    body {
        background: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .app-header {
        background-color: #4a90e2;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .app-footer {
        padding: 10px;
        text-align: center;
        font-size: 12px;
        color: #888;
        margin-top: 40px;
    }
    .prediction-box {
        background-color: white;
        padding: 25px;
        margin-top: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.3);
        text-align: center;
    }
    .input-label {
        font-weight: 600;
        margin-top: 15px;
        color: #333;
    }
    .submit-button {
        background-color: #4a90e2;
        border: none;
        color: white;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 25px;
        width: 100%;
    }
    .submit-button:hover {
        background-color: #357ABD;
    }
    .star-rating {
        color: #FFD700;
        font-size: 28px;
        cursor: pointer;
    }
    .sidebar-text {
        font-size: 14px;
        color: #555;
        line-height: 1.4;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="app-header">Insurance Premium Predictor</div>', unsafe_allow_html=True)

st.sidebar.title("About This App")
user_name = st.sidebar.text_input("Enter your name:")
st.sidebar.markdown(
    f"""
    Hello, **{user_name}!**  
    This app predicts your insurance premium based on several factors.
    """
)
st.sidebar.markdown("---")
st.sidebar.markdown("### Rate this app:")
rating = st.sidebar.select_slider("", options=[1, 2, 3, 4, 5], value=5, format_func=lambda x: "★" * x)
st.sidebar.markdown(f"<p class='star-rating'>{'★' * rating}{'☆' * (5 - rating)}</p>", unsafe_allow_html=True)
st.sidebar.markdown("Thank you for your feedback!")

# Building interractive interface for the API 
def predict_premium(input_data):
    url = "http://127.0.0.1:8000/predict"
    response = requests.post(url, json=input_data)
    if response.status_code == 200:
        return response.json().get("predicted_premium")
    else:
        st.error("Failed to get prediction from API.")
        return None

# frontend 
with st.form("input_form"):
    st.subheader("Enter Your Details")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    is_female = st.radio("Gender", options=[0, 1], format_func=lambda x: "Male" if x == 0 else "Female")
    bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=100.0, value=22.0, step=0.1)
    children = st.number_input("Number of Children", min_value=0, max_value=20, value=0)
    is_smoker = st.checkbox("Do you smoke?")
    region_southeast = st.checkbox("Living in Southeast region?")
    bmi_category_Obese = st.checkbox("Is your BMI category 'Obese'?")

    submit_button = st.form_submit_button("Predict Premium")

if submit_button:
    # Convert boolean checkboxes to int (0/1)
    input_json = {
        "age": age,
        "is_female": is_female,
        "bmi": bmi,
        "children": children,
        "is_smoker": int(is_smoker),
        "region_southeast": int(region_southeast),
        "bmi_category_Obese": int(bmi_category_Obese),
    }

    with st.spinner("Calculating your insurance premium..."):
        premium = predict_premium(input_json)

    if premium is not None:
        st.markdown(f'''
            <div class="prediction-box">
                <h3>Your Estimated Insurance Premium:</h3>
                <p style="font-size: 28px; color: #4a90e2; font-weight: bold;">${premium:,.2f}</p>
            </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="app-footer">© 2025 Insurance Prediction App | Built with Streamlit & FastAPI</div>', unsafe_allow_html=True)
