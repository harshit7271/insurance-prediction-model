from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
import joblib
import pandas as pd
from datetime import datetime

# Load model and scaler from pickle files
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# MLFlow
MODEL_VERSION = '1.0.0'

app = FastAPI()

# Pydantic model validate users input
class UserInput(BaseModel):
    age: float = Field(...)
    is_female: int = Field(..., description="1 for female, 0 for male")
    bmi: float = Field(...)
    children: int = Field(...)
    is_smoker: int = Field(..., description="1 if smoker, 0 if not")
    region_southeast: int = Field(..., description="1 if from southeast region, 0 otherwise")
    bmi_category_Obese: int = Field(..., description="1 if BMI category is Obese, 0 otherwise")

# these endpoints are human readable 
@app.get("/Hello")
def Hello():
    return JSONResponse(content={'message': 'Welcome to our Insurance Premium Prediction API'})

@app.get('/about')
def about():
    return JSONResponse(content={'message': 'A fully functional API to predict the premium amount of customers based on their region, BMI, smoking habits and age'})

@app.get('/')
def home():
    return JSONResponse(content={'message': 'Health Insurance Prediction API'})

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

def risk_category(premium):
    if premium < 3000:
        return "Low"
    elif premium < 6000:
        return "Medium"
    else:
        return "High"

@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'age': data.age,
        'is_female': data.is_female,
        'bmi': data.bmi,
        'children': data.children,
        'is_smoker': data.is_smoker,
        'region_southeast': data.region_southeast,
        'bmi_category_Obese': data.bmi_category_Obese
    }])
    to_scale = input_df[['age', 'bmi', 'children']]
    scaled = scaler.transform(to_scale)
    input_df[['age', 'bmi', 'children']] = scaled
    try:
        prediction = model.predict(input_df)[0]
        risk = risk_category(prediction)
        discount_eligibility = "Eligible" if data.is_smoker == 0 and data.bmi_category_Obese == 0 else "Not eligible"
        avg_premium_for_demo = 4000  # Hypothetical average
        comparison = "Above average" if prediction > avg_premium_for_demo else "Below average"

        response = {
            "predicted_premium": float(prediction),
            "risk_category": risk,
            "discount_eligibility": discount_eligibility,
            "comparison_to_average": comparison,
            "input_features": data.dict(),
            "model_version": MODEL_VERSION,
            "model_name": "Linear Regression",
            "status": "success"
        }
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})









