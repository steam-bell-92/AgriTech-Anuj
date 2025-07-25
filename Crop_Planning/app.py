# app.py
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyC4MuJYakQd4T-T74c6kfZ9KBpZNzukJ8Q"

try:
    genai.configure(api_key=API_KEY)
    genai_model = genai.GenerativeModel('gemini-2.0-flash')
    print("Google AI Model initialized successfully.")
except Exception as e:
    print(f"Error initializing Google AI Model: {e}")
    genai_model = None

def clean_ai_response(text_response):
    start = text_response.find('{')
    end = text_response.rfind('}')
    if start != -1 and end != -1:
        return text_response[start:end+1]
    return text_response

def get_ai_prediction_and_guide(user_data):
    if not genai_model:
        return json.dumps({"error": "AI model is not configured."})

    conditions = ", ".join([f"{key.replace('_', ' ')}: {value}" for key, value in user_data.items()])

    # FINAL, MOST STRICT PROMPT
    prompt = f"""
    You are a JSON API that provides agricultural advice.
    Your entire response MUST be a single, valid JSON object and nothing else.
    
    Analyze these farming conditions: {conditions}
    
    1.  Determine the single best crop that is appropriate for the "Season" provided.
    2.  Generate a farming guide for that crop. **IMPORTANT: For any lists or steps, use the newline character `\\n` to separate items.**
    
    Return a single JSON object with these exact keys: 
    "predicted_crop", "title", "how_to_plant", "fertilizer", "timeline", "ideal_rainfall", "post_harvest".
    """
    
    try:
        response = genai_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content from Gemini: {e}")
        return json.dumps({"error": "Failed to generate AI guide."})

@app.route('/')
def home():
    return render_template('cropplan.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        user_input_data = json_data['data']
        raw_ai_response = get_ai_prediction_and_guide(user_input_data)
        cleaned_json_string = clean_ai_response(raw_ai_response)

        try:
            ai_response_data = json.loads(cleaned_json_string)
            return jsonify({
                'crop': ai_response_data.get('predicted_crop', 'Unknown'),
                'guide_json_string': cleaned_json_string
            })
        except json.JSONDecodeError:
            return jsonify({'error': 'The AI returned an invalid response. Please try again.'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5003, debug=True)