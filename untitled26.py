
"""Untitled26.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ccV30cX45CVWdvymlZF9szLpDQbeXBHj
"""

import pandas as pd
df = pd.read_csv("/content/survey.csv")

# Explore the dataset
print(df.head())
print(df.info())

print(df.isnull().sum())

df = df.dropna(subset=["treatment"])

df["treatment"] = df["treatment"].apply(lambda x: 1 if x == "Yes" else 0)

features = ["Age", "Gender", "self_employed", "family_history", "work_interfere", "remote_work", "tech_company", "benefits", "care_options", "wellness_program", "seek_help", "anonymity", "leave", "mental_health_consequence", "phys_health_consequence", "coworkers", "supervisor", "mental_health_interview", "phys_health_interview", "mental_vs_physical", "obs_consequence"]
target = "treatment"

df = df[features + [target]]

df = pd.get_dummies(df, drop_first=True)

df.to_csv("cleaned_survey.csv", index=False)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("/content/cleaned_survey.csv")

X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
import joblib
joblib.dump(model, "mental_health_model.pkl")
import streamlit as st
import pandas as pd
import joblib
model = joblib.load("/content/mental_health_model.pkl")
st.title("Mental Health Treatment Prediction")
st.write("This app predicts whether an individual is likely to seek mental health treatment based on their survey responses.")
st.sidebar.header("User Input Features")
def user_input_features():
    age = st.sidebar.slider("Age", 18, 100, 30)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])  # Limit gender options to those seen during training
    family_history = st.sidebar.selectbox("Family History of Mental Illness", ["No", "Yes"])
    work_interfere = st.sidebar.selectbox("Work Interference", ["Never", "Rarely", "Sometimes", "Often"])
    remote_work = st.sidebar.selectbox("Remote Work", ["No", "Yes"])
    tech_company = st.sidebar.selectbox("Tech Company", ["No", "Yes"])
    benefits = st.sidebar.selectbox("Employer Provides Mental Health Benefits", ["No", "Yes", "Don't Know"])
    care_options = st.sidebar.selectbox("Care Options", ["No", "Yes", "Not Sure"])
    wellness_program = st.sidebar.selectbox("Wellness Program", ["No", "Yes", "Don't Know"])
    seek_help = st.sidebar.selectbox("Employer Provides Resources to Seek Help", ["No", "Yes", "Don't Know"])
    anonymity = st.sidebar.selectbox("Anonymity Protected", ["No", "Yes", "Don't Know"])
    leave = st.sidebar.selectbox("Ease of Medical Leave", ["Very Difficult", "Somewhat Difficult", "Somewhat Easy", "Very Easy"])
    mental_health_consequence = st.sidebar.selectbox("Mental Health Consequence", ["No", "Yes", "Maybe"])
    phys_health_consequence = st.sidebar.selectbox("Physical Health Consequence", ["No", "Yes", "Maybe"])
    coworkers = st.sidebar.selectbox("Discuss with Coworkers", ["No", "Yes", "Some of Them"])
    supervisor = st.sidebar.selectbox("Discuss with Supervisor", ["No", "Yes", "Some of Them"])
    mental_health_interview = st.sidebar.selectbox("Discuss in Interview", ["No", "Yes", "Maybe"])
    phys_health_interview = st.sidebar.selectbox("Physical Health in Interview", ["No", "Yes", "Maybe"])
    mental_vs_physical = st.sidebar.selectbox("Mental vs Physical Health", ["No", "Yes", "Don't Know"])
    obs_consequence = st.sidebar.selectbox("Observed Consequences", ["No", "Yes"])
    data = {
        "Age": age,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Gender_Other": 1 if gender == "Other" else 0,  
    }
    input_df = pd.DataFrame(data, index=[0])
    training_features = model.feature_names_in_
    input_df = input_df.reindex(columns=training_features, fill_value=0)

    return input_df
input_df = user_input_features()

st.subheader("User Input Features")
st.write(input_df)

prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)
st.subheader("Prediction")
st.write("Likely to seek treatment" if prediction[0] == 1 else "Not likely to seek treatment")
st.write("Prediction Probability:", prediction_proba)
