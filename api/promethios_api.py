import os
import sys
import json
import jsonschema
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Set up paths
PROMETHIOS_KERNEL_PATH = os.getenv("PROMETHIOS_KERNEL_PATH", "./promethios_core")
LOG_DIR = os.getenv("LOG_DIR", "../logs")
DATA_DIR = os.getenv("DATA_DIR", "../data")
WEB_URL = os.getenv("WEB_URL", "http://localhost:5002")

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Add Promethios core to path
sys.path.append(PROMETHIOS_KERNEL_PATH)

# Import Promethios core components
try:
    from governance_core import GovernanceCore
    from runtime_executor import RuntimeExecutor
except ImportError:
    print(f"Error: Could not import Promethios core components from {PROMETHIOS_KERNEL_PATH}")
    print("Please ensure PROMETHIOS_KERNEL_PATH is set correctly")
    sys.exit(1)

# Import pandas for data handling
try:
    import pandas as pd
except ImportError:
    print("Error: Could not import pandas")
    print("Please ensure pandas is installed")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title="Promethios Compliance API",
    description="API for the Promethios Compliance Demo",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema paths
SCHEMA_DIR = os.path.join(PROMETHIOS_KERNEL_PATH, "ResurrectionCodex", "schemas")
LOOP_EXECUTE_SCHEMA_PATH = os.path.join(SCHEMA_DIR, "loop_execute_request.schema.json")
OPERATOR_OVERRIDE_SCHEMA_PATH = os.path.join(SCHEMA_DIR, "operator_override_signal.schema.json")

# Load schemas
try:
    with open(LOOP_EXECUTE_SCHEMA_PATH, 'r') as f:
        loop_execute_request_schema = json.load(f)
    
    with open(OPERATOR_OVERRIDE_SCHEMA_PATH, 'r') as f:
        operator_override_schema = json.load(f)
except Exception as e:
    print(f"Error loading schemas: {e}")
    sys.exit(1)

# Runtime Executor Instance
runtime_executor = RuntimeExecutor()

# Helper for Schema Validation Error Response
def create_validation_error_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    error_details_list = []
    if isinstance(errors, jsonschema.exceptions.ValidationError):
        # Single top-level error
        error_details_list.append({
            "message": errors.message,
            "path": list(errors.path),
            "validator": errors.validator,
            "validator_value": errors.validator_value
        })
    elif isinstance(errors, list): # List of errors (e.g. from multiple checks)
        error_details_list = errors
    else: # Generic fallback
        error_details_list.append({"message": str(errors)})
    
    return JSONResponse(
        status_code=status_code,
        content={
            "request_id": "N/A", # Or try to get from request if possible
            "execution_status": "REJECTED",
            "governance_core_output": None,
            "emotion_telemetry": None,
            "justification_log": None,
            "error_details": {
                "code": "REQUEST_VALIDATION_ERROR",
                "message": "Request body failed schema validation.",
                "schema_validation_errors": error_details_list
            }
        }
    )

# API Endpoint: /loop/execute
@app.post("/loop/execute", 
        summary="Execute Governance Core Loop",
        description="Triggers the Promethios GovernanceCore loop with the provided plan and optional override signal.",
        tags=["Runtime Execution"])
async def execute_loop(request: Request):
    try:
        request_body = await request.json()
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "request_id": "N/A",
                "execution_status": "REJECTED",
                "error_details": {
                    "code": "INVALID_JSON",
                    "message": "Request body is not valid JSON."
                }
            }
        )
    
    # Validate request body
    try:
        jsonschema.validate(instance=request_body, schema=loop_execute_request_schema)
    except jsonschema.exceptions.ValidationError as e:
        return create_validation_error_response(e)
    except Exception as e:
        return create_validation_error_response(str(e))
    
    # Validate operator_override_signal if present
    operator_override_signal = request_body.get("operator_override_signal")
    if operator_override_signal is not None:
        try:
            jsonschema.validate(instance=operator_override_signal, schema=operator_override_schema)
        except jsonschema.exceptions.ValidationError as e:
            override_error = {
                "message": f"Operator override signal failed validation: {e.message}",
                "path": list(e.path),
                "validator": e.validator,
                "validator_value": e.validator_value
            }
            return create_validation_error_response([override_error])
        except Exception as e:
             return create_validation_error_response(str(e))
    
    # Execute the core loop
    response_data = runtime_executor.execute_core_loop(request_body)
    
    # Determine status code
    response_status_code = status.HTTP_200_OK
    if response_data.get("execution_status") == "FAILURE":
        response_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif response_data.get("execution_status") == "REJECTED":
        response_status_code = status.HTTP_400_BAD_REQUEST
    
    return JSONResponse(
        status_code=response_status_code,
        content=response_data
    )

# Root Endpoint for Health Check
@app.get("/", summary="Health Check", tags=["System"])
async def root():
    return {"message": "Promethios Compliance API is active."}

# Compliance API Endpoints
@app.get("/api/health", summary="API Health Check", tags=["Compliance"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "web_url": WEB_URL
    }

# Sample loan data for demo purposes
SAMPLE_LOAN_DATA = [
    {"id": "LC_1001", "loan_amount": 10000, "interest_rate": 5.32, "grade": "A", "employment_length": 10, "home_ownership": "RENT", "annual_income": 60000, "purpose": "debt_consolidation", "dti": 15.2, "delinq_2yrs": 0},
    {"id": "LC_1002", "loan_amount": 20000, "interest_rate": 10.99, "grade": "C", "employment_length": 3, "home_ownership": "OWN", "annual_income": 75000, "purpose": "home_improvement", "dti": 28.5, "delinq_2yrs": 1},
    {"id": "LC_1003", "loan_amount": 15000, "interest_rate": 7.89, "grade": "B", "employment_length": 5, "home_ownership": "MORTGAGE", "annual_income": 90000, "purpose": "major_purchase", "dti": 18.7, "delinq_2yrs": 0},
    {"id": "LC_1004", "loan_amount": 30000, "interest_rate": 15.23, "grade": "E", "employment_length": 1, "home_ownership": "RENT", "annual_income": 45000, "purpose": "debt_consolidation", "dti": 35.2, "delinq_2yrs": 3},
    {"id": "LC_1005", "loan_amount": 8000, "interest_rate": 6.08, "grade": "A", "employment_length": 8, "home_ownership": "OWN", "annual_income": 120000, "purpose": "credit_card", "dti": 10.1, "delinq_2yrs": 0}
]

# Store processed decisions in memory for demo
decisions_store = {}

# Direct implementation of compliance API endpoints
@app.get("/api/applications", summary="Get Loan Applications", tags=["Compliance"])
async def get_applications(count: int = 5):
    # Return sample loan data
    return SAMPLE_LOAN_DATA[:count]

@app.post("/api/process", summary="Process Loan Application", tags=["Compliance"])
async def process_application(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Get application ID
    application_id = data.get("application_id")
    if not application_id:
        raise HTTPException(status_code=400, detail="Missing application_id")
    
    # Get regulatory framework
    framework = data.get("framework", "EU_AI_ACT")
    
    # Get application data
    application = next((app for app in SAMPLE_LOAN_DATA if app["id"] == application_id), None)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    
    # Evaluate compliance (simplified for demo)
    compliance_result = evaluate_compliance(application, framework)
    
    # Generate decision ID
    decision_id = f"decision_{application_id}_{framework}"
    
    # Store decision
    decision = {
        "decision_id": decision_id,
        "application_id": application_id,
        "framework": framework,
        "timestamp": "2023-04-15T10:30:00Z",  # Fixed for demo
        "compliance_result": compliance_result,
        "application_data": application
    }
    
    decisions_store[decision_id] = decision
    
    return decision

@app.get("/api/decisions", summary="Get All Decisions", tags=["Compliance"])
async def get_decisions():
    return list(decisions_store.values())

@app.get("/api/decision/{decision_id}", summary="Get Decision by ID", tags=["Compliance"])
async def get_decision(decision_id: str):
    decision = decisions_store.get(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found")
    return decision

@app.get("/api/verify/{decision_id}", summary="Verify Decision Integrity", tags=["Compliance"])
async def verify_decision(decision_id: str):
    decision = decisions_store.get(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found")
    
    # For demo purposes, we'll just return a verification result
    return {
        "decision_id": decision_id,
        "verified": True,
        "verification_method": "cryptographic_hash",
        "timestamp": "2023-04-15T10:35:00Z"  # Fixed for demo
    }

# Helper function to evaluate compliance
def evaluate_compliance(application, framework):
    """Simplified compliance evaluation for demo purposes."""
    # Different compliance rules based on framework
    if framework == "EU_AI_ACT":
        # EU AI Act compliance check
        compliant = application["grade"] in ["A", "B"] and application["dti"] < 30
        details = "EU AI Act requires transparent decision-making and fair treatment."
        remediation = "Improve transparency in decision process and ensure non-discrimination."
    elif framework == "FINRA":
        # FINRA compliance check
        compliant = application["delinq_2yrs"] == 0 and application["dti"] < 35
        details = "FINRA requires proper risk assessment and disclosure."
        remediation = "Enhance risk assessment methodology and improve disclosures."
    else:
        # Internal compliance check
        compliant = application["loan_amount"] <= 25000 and application["interest_rate"] < 12
        details = "Internal policy requires conservative lending practices."
        remediation = "Adjust loan amount or interest rate to meet internal guidelines."
    
    return {
        "compliant": compliant,
        "details": details,
        "remediation": "" if compliant else remediation
    }

# Run the app if executed directly
if __name__ == "__main__":
    uvicorn.run("promethios_api:app", host="0.0.0.0", port=8002, reload=True)
