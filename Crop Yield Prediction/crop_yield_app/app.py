
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model and encoders
model = joblib.load('models/xgb_crop_model.pkl')
crop_encoder = joblib.load('models/Crop_encoder.pkl')
season_encoder = joblib.load('models/Season_encoder.pkl')
state_encoder = joblib.load('models/State_encoder.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form = request.form

        # Parse form inputs
        crop = form['crop']
        year = int(form['year'])
        season = form['season']
        state = form['state']
        area = float(form['area'])
        production = float(form['production'])
        rainfall = float(form['rainfall'])

        # Encode values
        if crop not in crop_encoder.classes_:
            return jsonify({'success': False, 'error': f"Unknown crop: {crop}"}), 400
        if season not in season_encoder.classes_:
            return jsonify({'success': False, 'error': f"Unknown season: {season}"}), 400
        if state not in state_encoder.classes_:
            return jsonify({'success': False, 'error': f"Unknown state: {state}"}), 400

        crop_encoded = crop_encoder.transform([crop])[0]
        season_encoded = season_encoder.transform([season])[0]
        state_encoded = state_encoder.transform([state])[0]

        # Prepare features
        features = np.array([[crop_encoded, year, season_encoded, state_encoded, area, rainfall, production]])

        # Predict
        prediction = float(round(model.predict(features)[0], 2))

        # Return result
        return jsonify({
            'success': True,
            'prediction': prediction,
            'context': {
                'efficiency': "Moderate",
                'efficiency_note': "Yield efficiency is average.",
                'rainfall_impact': "Positive",
                'rainfall_note': "Rainfall is within optimal range.",
                'recommendation': "Consider using improved seeds for better yield.",
                'season_tip': "Ensure timely sowing for the selected season."
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5502)