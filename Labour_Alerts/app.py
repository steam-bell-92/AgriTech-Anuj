from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # <-- This line enables CORS for all routes

@app.route('/news')
def get_news():
    api_key = 'pub_9a1996b402894fa081be406a87c64f36' 
    api_url = f'https://newsdata.io/api/1/latest?apikey=pub_9a1996b402894fa081be406a87c64f36&qInMeta=farming&language=hi&country=in'

    response = requests.get(api_url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
