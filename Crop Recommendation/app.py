from flask import Flask, render_template, request, send_file
import joblib
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime

app = Flask(__name__)
model = joblib.load('model/rf_model.pkl')
label_encoder = joblib.load('model/label_encoder.pkl')  # Load encoder

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['ph']),
            float(request.form['rainfall'])
        ]
        input_params = {
            'N': request.form['N'],
            'P': request.form['P'],
            'K': request.form['K'],
            'temperature': request.form['temperature'],
            'humidity': request.form['humidity'],
            'ph': request.form['ph'],
            'rainfall': request.form['rainfall']
        }
        prediction_num = model.predict([data])[0]
        prediction_label = label_encoder.inverse_transform([prediction_num])[0]  # Convert to name
        return render_template('result.html', crop=prediction_label, params=input_params)
    except Exception as e:
        return f"Error: {e}"


# PDF download route
@app.route('/download_report', methods=['POST'])
def download_report():
    try:
        crop = request.form['crop']
        params = {
            'N': request.form['N'],
            'P': request.form['P'],
            'K': request.form['K'],
            'temperature': request.form['temperature'],
            'humidity': request.form['humidity'],
            'ph': request.form['ph'],
            'rainfall': request.form['rainfall']
        }
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        # Logo/Header (optional)
        p.setFont('Helvetica-Bold', 18)
        p.drawString(50, height - 60, "AgriTech Crop Recommendation Report")
        # Date & Time
        p.setFont('Helvetica', 10)
        p.drawString(50, height - 80, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # Input Parameters
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, height - 120, "Input Parameters:")
        p.setFont('Helvetica', 11)
        y = height - 140
        for k, v in params.items():
            p.drawString(70, y, f"{k}: {v}")
            y -= 18
        # Prediction Result
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, y - 10, "Prediction Result:")
        p.setFont('Helvetica', 13)
        p.drawString(70, y - 30, f"Recommended Crop: {crop}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="crop_recommendation_report.pdf", mimetype='application/pdf')
    except Exception as e:
        return f"Error generating PDF: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5501)
