from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # <-- This line enables CORS for all routes

# Security configuration
API_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1  # seconds between requests

# Cache for API responses to reduce API calls
api_cache = {}
cache_duration = 300  # 5 minutes

@app.route('/news')
def get_news():
    try:
        # Check cache first
        current_time = time.time()
        if 'news_data' in api_cache and (current_time - api_cache['timestamp']) < cache_duration:
            return jsonify(api_cache['news_data'])
        
        api_key = 'pub_9a1996b402894fa081be406a87c64f36' 
        api_url = f'https://newsdata.io/api/1/latest?apikey={api_key}&qInMeta=farming&language=hi&country=in'

        # Add retry logic with exponential backoff
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(api_url, timeout=API_TIMEOUT)
                response.raise_for_status()
                
                # Cache the response
                api_cache['news_data'] = response.json()
                api_cache['timestamp'] = current_time
                
                return jsonify(response.json())
                
            except requests.Timeout:
                if attempt == MAX_RETRIES - 1:
                    app.logger.error("API request timed out after all retries")
                    return jsonify({'error': 'News service temporarily unavailable'}), 503
                time.sleep(RATE_LIMIT_DELAY * (2 ** attempt))  # Exponential backoff
                
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    app.logger.error(f"API request failed: {str(e)}")
                    return jsonify({'error': 'News service unavailable'}), 503
                time.sleep(RATE_LIMIT_DELAY * (2 ** attempt))
                
    except Exception as e:
        app.logger.error(f"News API error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Global error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({'error': 'Service temporarily unavailable'}), 503

if __name__ == '__main__':
    app.run(port=5000, debug=True)
