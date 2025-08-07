from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
from utils import load_keras_model, predict_image_keras
import os
import requests

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')


# Route for homepage


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/farmer')
def farmer():
    return render_template('farmer.html')


@app.route('/disease')
def disease():
    return render_template('disease.html')


@app.route('/organic')
def organic():
    return render_template('organic.html')


@app.route('/shopkeeper')
def shopkeeper():
    return render_template('shopkeeper.html')


@app.route('/plantation')
def plantation():
    return render_template('plantation.html')


@app.route('/feedback')
def feedback():
    return render_template('feed-back.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')

# New API route to act as a secure proxy


@app.route('/api/chat', methods=['POST'])
def api_chat():
    # Get the message history from the client-side request
    data = request.json
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not gemini_api_key:
        return jsonify({"error": "API key not configured on the server"}), 500

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={gemini_api_key}"

    try:
        # Make the request to the actual Gemini API from the server
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to communicate with the AI service."}), 502


# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded."
    file = request.files['file']
    if file.filename == '':
        return "No selected file."

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    predicted_class, description = predict_image_keras(model, filepath)

    return render_template('result.html',
                           prediction=predicted_class,
                           description=description,
                           image_path=filepath)


if __name__ == '__main__':
    app.run(debug=True)
