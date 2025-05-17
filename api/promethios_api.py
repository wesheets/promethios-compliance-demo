import os
import sys
import json
import time
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from compliance_api.compliance_wrapper import ComplianceWrapper
from compliance_api.analysis_logger import AnalysisLogger
from compliance_api.openai_explainer import OpenAIExplainer
from compliance_api.pdf_report_generator import PDFReportGenerator

app = Flask(__name__)
CORS(app)

# Initialize components
compliance_wrapper = ComplianceWrapper()
analysis_logger = AnalysisLogger()
openai_explainer = OpenAIExplainer()
pdf_generator = PDFReportGenerator()

# In-memory storage for demo purposes
applications = []
decisions = {}
session_contexts = {}

# Load sample applications
def load_sample_applications():
    return [
        {
            "id": "LC_1001",
            "amount": 10000,
            "purpose": "debt_consolidation",
            "grade": "A"
        },
        {
            "id": "LC_1002",
            "amount": 20000,
            "purpose": "home_improvement",
            "grade": "C"
        },
        {
            "id": "LC_1003",
            "amount": 15000,
            "purpose": "major_purchase",
            "grade": "B"
        },
        {
            "id": "LC_1004",
            "amount": 30000,
            "purpose": "debt_consolidation",
            "grade": "E"
        },
        {
            "id": "LC_1005",
            "amount": 5000,
            "purpose": "credit_card",
            "grade": "A"
        }
    ]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/api/applications', methods=['GET'])
def get_applications():
    global applications
    if not applications:
        applications = load_sample_applications()
    return jsonify(applications)

@app.route('/api/evaluate/<application_id>/<framework>', methods=['POST'])
def evaluate_application(application_id, framework):
    global applications, decisions
    
    # Find the application
    app_list = applications if applications else load_sample_applications()
    application = next((app for app in app_list if app["id"] == application_id), None)
    
    if not application:
        return jsonify({"error": "Application not found"}), 404
    
    # Log the start of evaluation
    analysis_logger.log_event(
        "compliance_decision", 
        f"Starting evaluation of application {application_id} against {framework}",
        {"application_id": application_id, "framework": framework}
    )
    
    # Perform the evaluation
    try:
        result = compliance_wrapper.evaluate(application, framework)
        
        # Generate a decision ID
        decision_id = f"decision_{application_id}_{framework}"
        
        # Store the decision
        decisions[decision_id] = {
            "application": application,
            "framework": framework,
            "result": result,
            "timestamp": time.time()
        }
        
        # Log the completion of evaluation
        analysis_logger.log_event(
            "compliance_decision", 
            f"Completed evaluation of application {application_id}",
            {"application_id": application_id, "framework": framework, "decision_id": decision_id, "result": result}
        )
        
        return jsonify({
            "decision_id": decision_id,
            "result": result
        })
    except Exception as e:
        # Log the error
        analysis_logger.log_event(
            "error", 
            f"Error evaluating application {application_id}: {str(e)}",
            {"application_id": application_id, "framework": framework, "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/decision/<decision_id>', methods=['GET'])
def get_decision(decision_id):
    if decision_id not in decisions:
        return jsonify({"error": "Decision not found"}), 404
    
    return jsonify(decisions[decision_id])

@app.route('/api/explain', methods=['POST'])
def explain_decision():
    data = request.json
    decision_id = data.get('decision_id')
    query = data.get('query', '')
    
    if not decision_id or decision_id not in decisions:
        return jsonify({"error": "Decision not found"}), 404
    
    # Log the explanation request
    analysis_logger.log_event(
        "explanation_request", 
        f"Explanation requested for decision {decision_id}",
        {"decision_id": decision_id, "query": query}
    )
    
    try:
        # Get the decision data
        decision_data = decisions[decision_id]
        
        # Generate explanation
        explanation = openai_explainer.explain_decision(decision_data, query)
        
        # Log the explanation response
        analysis_logger.log_event(
            "explanation_response", 
            f"Explanation generated for decision {decision_id}",
            {"decision_id": decision_id, "query": query}
        )
        
        return jsonify({"explanation": explanation})
    except Exception as e:
        # Log the error
        analysis_logger.log_event(
            "error", 
            f"Error generating explanation for decision {decision_id}: {str(e)}",
            {"decision_id": decision_id, "query": query, "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4()))
    context = data.get('context', {})
    
    # Store or update session context
    session_contexts[session_id] = context
    
    # Log the chat request
    analysis_logger.log_event(
        "chat_request", 
        f"Chat message received: {message}",
        {"session_id": session_id, "message": message, "context": context}
    )
    
    try:
        # Get relevant decision context if available
        decision_context = None
        if 'decision_id' in context and context['decision_id'] in decisions:
            decision_context = decisions[context['decision_id']]
        
        # Process the chat message
        response, success = openai_explainer.chat(message, session_id, context)
        
        # Log the chat response
        analysis_logger.log_event(
            "chat_response", 
            f"Chat response generated",
            {"session_id": session_id, "success": success}
        )
        
        return jsonify({"response": response, "session_id": session_id})
    except Exception as e:
        # Log the error
        analysis_logger.log_event(
            "error", 
            f"Error processing chat message: {str(e)}",
            {"session_id": session_id, "message": message, "error": str(e)}
        )
        return jsonify({
            "response": "I apologize, but I'm having trouble processing your request. Please try again in a moment.",
            "session_id": session_id
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Get query parameters
    log_type = request.args.get('type')
    limit = int(request.args.get('limit', 50))
    
    # Get logs
    logs = analysis_logger.get_logs(log_type, limit)
    
    return jsonify(logs)

@app.route('/api/report/<decision_id>', methods=['GET'])
def generate_report(decision_id):
    if decision_id not in decisions:
        return jsonify({"error": "Decision not found"}), 404
    
    # Log the report generation request
    analysis_logger.log_event(
        "report_generation", 
        f"Report generation requested for decision {decision_id}",
        {"decision_id": decision_id}
    )
    
    try:
        # Get the decision data
        decision_data = decisions[decision_id]
        
        # Generate the report
        report_path = pdf_generator.generate_report(decision_data)
        
        # Log the report generation completion
        analysis_logger.log_event(
            "report_generation", 
            f"Report generated for decision {decision_id}",
            {"decision_id": decision_id, "report_path": report_path}
        )
        
        return send_file(report_path, as_attachment=True, download_name=f"compliance_report_{decision_id}.pdf")
    except Exception as e:
        # Log the error
        analysis_logger.log_event(
            "error", 
            f"Error generating report for decision {decision_id}: {str(e)}",
            {"decision_id": decision_id, "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

# Alias for the report endpoint to match frontend expectations
@app.route('/api/generate-report/<decision_id>', methods=['GET'])
def generate_report_alias(decision_id):
    return generate_report(decision_id)

if __name__ == '__main__':
    # Load sample applications
    applications = load_sample_applications()
    
    # Start the server
    app.run(host='0.0.0.0', port=8001, debug=True)
