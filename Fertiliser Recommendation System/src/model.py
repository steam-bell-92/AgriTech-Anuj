# src/model.py

import joblib
import pandas as pd

# Load model and encoders
model = joblib.load('../saved_model/fertilizer_model.pkl')
soil_encoder = joblib.load('../saved_model/soil_encoder.pkl')
crop_encoder = joblib.load('../saved_model/crop_encoder.pkl')
fertilizer_encoder = joblib.load('../saved_model/fertilizer_encoder.pkl')

def decode_fertilizer(encoded_label):
    return fertilizer_encoder.inverse_transform([encoded_label])[0]

def predict_fertilizer(temparature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous):
    # Encode categorical inputs
    soil_type_encoded = soil_encoder.transform([soil_type])[0]
    crop_type_encoded = crop_encoder.transform([crop_type])[0]

    # Create input data matching training feature names exactly
    input_data = pd.DataFrame([[
        temparature, humidity, moisture,
        soil_type_encoded, crop_type_encoded,
        nitrogen, potassium, phosphorous
    ]], columns=[
        'Temparature', 'Humidity ', 'Moisture',
        'Soil Type', 'Crop Type',
        'Nitrogen', 'Potassium', 'Phosphorous'
    ])

    # Predict and decode fertilizer name
    pred = model.predict(input_data)[0]
    return decode_fertilizer(pred)
