from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
import json
import jsonschema # For request validation
import os
import uuid

from runtime_executor import RuntimeExecutor, load_schema # Assuming runtime_executor.py is in the same directory or accessible

# --- FastAPI App Initialization --- #
app = FastAPI(
    title="Promethios Governance Core Runtime",
    version="2.1.0",
    description="HTTP API for executing the Promethios GovernanceCore loop."
)

# --- Schema Loading for Request Validation --- #
# These paths assume main.py is in the root of promethios_repo
SCHEMA_BASE_PATH = os.path.join(os.path.dirname(__file__), "ResurrectionCodex")
API_SCHEMA_PATH = os.path.join(SCHEMA_BASE_PATH, "02_System_Architecture", "API_Schemas")
MGC_SCHEMA_PATH = os.path.join(SCHEMA_BASE_PATH, "01_Minimal_Governance_Core_MGC", "MGC_Schema_Registry")

LOOP_EXECUTE_REQUEST_SCHEMA_PATH = os.path.join(API_SCHEMA_PATH, "loop_execute_request.v1.schema.json")
OPERATOR_OVERRIDE_SCHEMA_PATH = os.path.join(MGC_SCHEMA_PATH, "operator_override.schema.v1.json")

loop_execute_request_schema = load_schema(LOOP_EXECUTE_REQUEST_SCHEMA_PATH)
operator_override_schema = load_schema(OPERATOR_OVERRIDE_SCHEMA_PATH)

# --- Runtime Executor Instance --- #
runtime_executor = RuntimeExecutor()

# --- Helper for Schema Validation Error Response --- #
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

# --- API Endpoint: /loop/execute --- #
@app.post("/loop/execute", 
            # response_model can be defined with Pydantic if schemas are converted,
            # but batch plan focuses on JSON schemas directly.
            # For now, response structure is handled by runtime_executor.
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

    # Codex Check 1.1: Validate entire request body
    try:
        jsonschema.validate(instance=request_body, schema=loop_execute_request_schema)
    except jsonschema.exceptions.ValidationError as e:
        return create_validation_error_response(e)
    except Exception as e: # Catch other potential errors during validation
        return create_validation_error_response(str(e))

    # Codex Check 1.2: Validate operator_override_signal if present
    operator_override_signal = request_body.get("operator_override_signal")
    if operator_override_signal is not None: # Ensure it's not just present but also not null if schema expects object
        try:
            jsonschema.validate(instance=operator_override_signal, schema=operator_override_schema)
        except jsonschema.exceptions.ValidationError as e:
            # Specific error for override signal validation failure
            override_error = {
                "message": f"Operator override signal failed validation: {e.message}",
                "path": list(e.path),
                "validator": e.validator,
                "validator_value": e.validator_value
            }
            return create_validation_error_response([override_error])
        except Exception as e:
             return create_validation_error_response(str(e))

    # If all input validations pass, proceed to execute the core loop
    # The runtime_executor handles its own output validations and error structuring.
    # Task 2.1.5.1: Logging within runtime_executor
    # Task 2.1.6 & Codex Checks 5.1, 5.2, 5.3 are handled by runtime_executor and GC structure
    response_data = runtime_executor.execute_core_loop(request_body)
    
    # Determine status code based on execution_status from executor
    # This is a simple mapping, could be more nuanced
    response_status_code = status.HTTP_200_OK
    if response_data.get("execution_status") == "FAILURE":
        response_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # Or 422 if it's a processing error of valid data
    elif response_data.get("execution_status") == "REJECTED":
        response_status_code = status.HTTP_400_BAD_REQUEST # Should have been caught earlier, but as a fallback

    return JSONResponse(
        status_code=response_status_code,
        content=response_data
    )

# --- Root Endpoint for Health Check (Optional) --- #
@app.get("/", summary="Health Check", tags=["System"])
async def root():
    return {"message": "Promethios Governance Core Runtime is active."}

# --- To run locally (for development) --- #
# uvicorn main:app --reload --port 8000

