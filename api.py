from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd

# Load model and scaler from pickle files
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

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


@app.get("/Hello")
def Hello():
    return JSONResponse(content= {'message' : 'Welcome to our Insurance Premium Prediction API'})

@app.get('/about')
def about():
    return JSONResponse(content={'message': 'A fully functional API to predict the premium amount of customers based on their region, BMI, smoking habits and age'})

@app.post("/predict")
def predict_premium(data: UserInput):
    # Convert input data to DataFrame in correct column order for model
    input_df = pd.DataFrame([{
        'age': data.age,
        'is_female': data.is_female,
        'bmi': data.bmi,
        'children': data.children,
        'is_smoker': data.is_smoker,
        'region_southeast': data.region_southeast,
        'bmi_category_Obese': data.bmi_category_Obese
    }])

    # Scale only the columns required by scaler
    to_scale = input_df[['age', 'bmi', 'children']]
    scaled = scaler.transform(to_scale)

    # Replace scaled columns with scaled values
    input_df[['age', 'bmi', 'children']] = scaled

    # Predict using the model
    prediction = model.predict(input_df)[0]

    return {"predicted_premium": float(prediction)}
         




