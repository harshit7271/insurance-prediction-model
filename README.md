# 🏥 Insurance Prediction Model  
## 🚀 Live Demo

You can try out the **Insurance Premium Prediction** app live and even edit the code or explore it interactively.

- **Live Demo:**  
  [![Open Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=streamlit)](https://insurance-prediction-model-y4xggsjhsnqsj2jlddmxjb.streamlit.app/)

---
A **Machine Learning project** built with **Linear Regression** to predict **insurance charges** based on user attributes such as age, BMI, smoking status, region, and other factors.  
---
## 📊 Exploratory Data Analysis (EDA)
- Thorough **EDA performed** to understand relationships in the dataset  
- Visualized distributions and patterns using **Seaborn & Matplotlib**  
- Insights:  
  - Smokers tend to have significantly higher charges  
  - BMI and age are strong predictors of insurance cost  
  - Regional differences are minimal but present  

---

## 🎨 Data Visualization
- **Heatmaps & pair plots** for correlation analysis  
- **Scatter plots** to understand age, BMI vs charges  
- **Box plots** to show outliers and categorical impact (smoker, region, sex)  

---

## 🧹 Data Preprocessing
- Encoded categorical features using **Label Encoding / One-Hot Encoding**  
- Applied **StandardScaler** to normalize continuous features (age, BMI, children)  
- Used **SciPy** for statistical analysis and initial data insights  
- Null/missing values checked and cleaned before training  

---

## 🚀 Project Highlights
- Implements **Linear Regression** algorithm from scikit-learn  
- Predicts  **medical insurance premium charges** with solid accuracy  
- Evaluated using **R²** and **Adjusted R²**  
- Data processing pipeline ensures reproducibility  

---

## 🧑‍💻 Tech Stack
- Python 3.x  
- Pandas, NumPy  
- Scikit-Learn (Linear Regression, preprocessing via StandardScaler)  
- Matplotlib, Seaborn (visualizations)  
- SciPy (statistical analysis)  

---

## 📊 Model Performance
- Train/Test split for fair evaluation  
- **R² score:** 79% on unseen test data  
- **Adjusted R² score:** 80%  

---

## 📂 Project Structure
📁 Insurance-Prediction

┣ 📄 insurance.csv # Dataset

┣ 📄 insurance_model.ipynb # EDA + Preprocessing + Model Training

┣ 📄 model.pkl # Saved regression model

┣ 📄 requirements.txt # Dependencies list

┗ 📄 README.md # Project documentation


---

## ⚡ How to Run
1. Clone this repository  
git clone https://github.com/harshit7271/insurance-prediction-model


2. Install dependencies  
pip install -r requirements.txt


3. Run the notebook/script for analysis and predictions  
jupyter notebook insurance-prediction-model.ipynb


---

## 📌 Future Improvements
- Test advanced ML models like Random Forest, XGBoost, Gradient Boosting  
- Hyperparameter tuning for better performance  
- Build UI for deployment (Streamlit / FastAPI app)  
- Add cross-validation and feature importance analysis  

---

## ✨ Results
✔️ Linear Regression achieved **79% R²** and **80% Adjusted R²**  
✔️ **EDA revealed critical feature importance (age, BMI, smoker)**  
✔️ Scaled & preprocessed data improved accuracy and model consistency  

---

## 🏆 Author
👨‍💻 Developed by [HARSHIT SINGH] – Passionate about ML, data-driven insights, and AI model deployment.  

