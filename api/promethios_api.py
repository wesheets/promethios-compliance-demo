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

# Import Compliance API components
try:
    sys.path.append("./compliance_api")
    from compliance_api.compliance_api import app as compliance_app
    from compliance_api.compliance_wrapper import ComplianceWrapper
    from compliance_api.data_loader import LoanDataLoader
except ImportError as e:
    print(f"Error: Could not import Compliance API components: {e}")
    print("Please ensure compliance_api directory is available")
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

# Include all routes from the compliance API
# Mount the compliance API routes
from fastapi import APIRouter
compliance_router = APIRouter()

@compliance_router.get("/api/applications", summary="Get Loan Applications", tags=["Compliance"])
async def get_applications(count: int = 5):
    data_loader = LoanDataLoader()
    applications = data_loader.load_loan_applications(count)
    return applications

@compliance_router.post("/api/process", summary="Process Loan Application", tags=["Compliance"])
async def process_application(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    data_loader = LoanDataLoader()
    compliance_wrapper = ComplianceWrapper()
    
    # Get application ID
    application_id = data.get("application_id")
    if not application_id:
        raise HTTPException(status_code=400, detail="Missing application_id")
    
    # Get regulatory framework
    framework = data.get("framework", "GDPR")
    
    # Get application data
    application = data_loader.get_application_by_id(application_id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    
    # Evaluate compliance
    compliance_result = compliance_wrapper.evaluate_compliance(application, framework)
    
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
    
    # For demo purposes, we'll just return the decision
    return decision

@compliance_router.get("/api/decisions", summary="Get All Decisions", tags=["Compliance"])
async def get_decisions():
    # For demo purposes, return an empty list
    return []

@compliance_router.get("/api/decision/{decision_id}", summary="Get Decision by ID", tags=["Compliance"])
async def get_decision(decision_id: str):
    # For demo purposes, return a not found error
    raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found")

@compliance_router.get("/api/verify/{decision_id}", summary="Verify Decision Integrity", tags=["Compliance"])
async def verify_decision(decision_id: str):
    # For demo purposes, return a not found error
    raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found")

# Include the compliance router in the main app
app.include_router(compliance_router)

# Run the app if executed directly
if __name__ == "__main__":
    uvicorn.run("promethios_api:app", host="0.0.0.0", port=8002, reload=True)
