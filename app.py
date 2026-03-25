import streamlit as st
import pandas as pd
import pickle
import requests

API_URL = "https://car-price-predictor-backend-er0t.onrender.com/predict"
# API_URL = "http://127.0.0.1:8080/predict"


st.title('Car price prediction app')
cars = pickle.load(open("cars.pkl","rb"))


name = st.selectbox(
    "Enter car name",
    cars['name'].unique(),
    index=None,
    placeholder='Car Name'
)

company = st.selectbox(
    "Enter the name of the company",
    cars['company'].unique(),
    index=None,
    placeholder="Company Name"
)

year = st.number_input(
    "Enter the year in which you buy this car",
    value=2010,
    placeholder="Type a year.."
)

kms_driven = st.number_input(
    "How much distance this car travel",
    value=1000,
)

fuel_type = st.selectbox(
    "Which type of fuel this car use",
    cars['fuel_type'].unique(),
)

if st.button('Predict'):
    input_data = {
        "name":name,
        "company":company,
        "year":year,
        "kms_driven":kms_driven,
        "fuel_type":fuel_type
    }
    try:
        response = requests.post(API_URL,json = input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted car price : {result["prediction"]}")
        else:
            error = response.json()["detail"][0]["msg"]
            st.error(error)
    except requests.exceptions.ConnectionError:
        st.error("could not connect to the fast api server")