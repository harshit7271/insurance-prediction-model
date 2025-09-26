from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from schema.user_input import UserInput
import numpy as np
import joblib
import pandas as pd
from datetime import datetime

# Load model and scaler from pickle files
model = joblib.load('model/model.pkl')
scaler = joblib.load('model/scaler.pkl')


# MLFlow
MODEL_VERSION = '1.0.0'

app = FastAPI()

# Define Pydantic model for input validation
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
    return JSONResponse(content= {'message' : 'Welcome to our Insurance Premium Prediction API'})


@app.get('/about')
def about():
    return JSONResponse(content={'message': 'A fully functional API to predict the premium amount of customers based on their region, BMI, smoking habits and age'})


@app.get('/')
def home():
    return JSONResponse(content= {'message' : 'Health Insurance Prediction API'})


# machine readable
@app.get('/health')
def health_check():
    return {
        'status' : 'OK',
        'version' : 'MODEL_VERSION',
        'model_loaded' : model is not None
    }
    
# Input endpoint
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
        response = {
            "predicted_premium": float(prediction),
            "model_version": MODEL_VERSION,
            "input_features": data.dict(),
            "explanation": "The premium is estimated based on age, BMI, smoking status, gender, region, and BMI category. Higher age, smoking, and BMI generally increase premiums.",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "model_name": "Linear Regression",
            "status": "success"
        }
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})







