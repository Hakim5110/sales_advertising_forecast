import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('linear_regression_model.sav')

st.title('Sales Prediction using Linear Regression')
st.write('Enter the advertising spending for TV, Radio, and Newspaper to predict sales.')

# Input fields for features
tv = st.number_input('TV Advertising Spend', min_value=0.0, max_value=300.0, value=100.0, step=0.1)
radio = st.number_input('Radio Advertising Spend', min_value=0.0, max_value=50.0, value=20.0, step=0.1)
newspaper = st.number_input('Newspaper Advertising Spend', min_value=0.0, max_value=120.0, value=30.0, step=0.1)

if st.button('Predict Sales'):
    # Create a DataFrame for the input
    input_data = pd.DataFrame([{
        'TV': tv,
        'Radio': radio,
        'Newspaper': newspaper
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]

    st.success(f'Predicted Sales: {prediction:.2f}')
