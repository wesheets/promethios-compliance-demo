from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
import os
import requests
import json
from datetime import datetime
import io
import base64
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Load environment variables
API_URL = os.environ.get('API_URL', 'http://localhost:8000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compliance-officer')
def compliance_officer_dashboard():
    return render_template('compliance_officer.html')

@app.route('/data-scientist')
def data_scientist_dashboard():
    return render_template('data_scientist.html')

@app.route('/executive')
def executive_dashboard():
    return render_template('executive.html')

@app.route('/api/applications')
def get_applications():
    try:
        response = requests.get(f"{API_URL}/api/applications")
        if response.status_code == 200:
            applications = response.json()
            # Ensure applications is always an array
            if not isinstance(applications, list):
                if isinstance(applications, dict) and 'applications' in applications:
                    applications = applications['applications']
                else:
                    applications = []
            return jsonify(applications)
        else:
            return jsonify({"error": f"Error fetching applications: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading applications: {str(e)}"}), 500

@app.route('/api/process', methods=['POST'])
def process_application():
    try:
        data = request.json
        application_id = data.get('application_id')
        framework = data.get('framework', 'EU_AI_ACT')
        
        response = requests.post(
            f"{API_URL}/api/process",
            json={"application_id": application_id, "framework": framework}
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error processing application: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error processing application: {str(e)}"}), 500

@app.route('/api/decisions')
def get_decisions():
    try:
        response = requests.get(f"{API_URL}/api/decisions")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error fetching decisions: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading decisions: {str(e)}"}), 500

@app.route('/api/decision/<decision_id>')
def get_decision(decision_id):
    try:
        response = requests.get(f"{API_URL}/api/decision/{decision_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error fetching decision: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading decision: {str(e)}"}), 500

@app.route('/api/verify/<decision_id>')
def verify_decision(decision_id):
    try:
        response = requests.get(f"{API_URL}/api/verify/{decision_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error verifying decision: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error verifying decision: {str(e)}"}), 500

@app.route('/api/explain', methods=['POST'])
def explain_decision():
    try:
        data = request.json
        decision_id = data.get('decision_id')
        query = data.get('query', '')
        
        response = requests.post(
            f"{API_URL}/api/explain",
            json={"decision_id": decision_id, "query": query}
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error getting explanation: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error getting explanation: {str(e)}"}), 500

@app.route('/api/trust-factors/<application_id>')
def get_trust_factors(application_id):
    try:
        response = requests.get(f"{API_URL}/api/trust-factors/{application_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error fetching trust factors: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading trust factors: {str(e)}"}), 500

@app.route('/api/recommendations/<application_id>')
def get_recommendations(application_id):
    try:
        response = requests.get(f"{API_URL}/api/recommendations/{application_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error fetching recommendations: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading recommendations: {str(e)}"}), 500

@app.route('/api/generate-report/<decision_id>')
def generate_report(decision_id):
    try:
        response = requests.get(f"{API_URL}/api/generate-report/{decision_id}")
        if response.status_code == 200:
            report_data = response.json()
            
            # If the API returns PDF data as base64
            if 'pdf_data' in report_data:
                pdf_data = base64.b64decode(report_data['pdf_data'])
                return send_file(
                    io.BytesIO(pdf_data),
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f"compliance_report_{decision_id}.pdf"
                )
            else:
                return jsonify(report_data)
        else:
            return jsonify({"error": f"Error generating report: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error generating report: {str(e)}"}), 500

@app.route('/api/timeline/<application_id>')
def get_timeline(application_id):
    try:
        response = requests.get(f"{API_URL}/api/timeline/{application_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error fetching timeline: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error loading timeline: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
