import os
import requests
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8002")

# Create Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/applications', methods=['GET'])
def get_applications():
    count = request.args.get('count', 5, type=int)
    
    # Forward request to API
    response = requests.get(f"{API_URL}/api/applications?count={count}")
    
    if response.status_code == 200:
        applications = response.json()
        # Ensure we're returning an array
        if not isinstance(applications, list):
            # If it's not a list, check if it might be wrapped in an object
            if isinstance(applications, dict) and 'applications' in applications:
                applications = applications['applications']
            else:
                # If we can't extract an array, return an empty array
                applications = []
        return jsonify(applications)
    else:
        return jsonify({"error": "Failed to fetch applications"}), response.status_code

@app.route('/api/process', methods=['POST'])
def process_application():
    data = request.json
    
    # Forward request to API
    response = requests.post(f"{API_URL}/api/process", json=data)
    
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to process application"}), response.status_code

@app.route('/api/decisions', methods=['GET'])
def get_decisions():
    # Forward request to API
    response = requests.get(f"{API_URL}/api/decisions")
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch decisions"}), response.status_code

@app.route('/api/decision/<decision_id>', methods=['GET'])
def get_decision(decision_id):
    # Forward request to API
    response = requests.get(f"{API_URL}/api/decision/{decision_id}")
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Decision not found"}), response.status_code

@app.route('/api/verify/<decision_id>', methods=['GET'])
def verify_decision(decision_id):
    # Forward request to API
    response = requests.get(f"{API_URL}/api/verify/{decision_id}")
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to verify decision"}), response.status_code

@app.route('/health')
def health():
    # Check API health
    try:
        response = requests.get(f"{API_URL}/")
        api_status = "connected" if response.status_code == 200 else "error"
    except:
        api_status = "unreachable"
    
    return jsonify({
        "status": "healthy",
        "api_status": api_status,
        "api_url": API_URL
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5002)))
