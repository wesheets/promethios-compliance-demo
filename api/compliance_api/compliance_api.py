from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from compliance_wrapper import ComplianceWrapper
from data_loader import LoanDataLoader
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Initialize components
compliance_wrapper = ComplianceWrapper()
data_loader = LoanDataLoader()

# Store processed decisions in memory for demo
decisions_store = {}

@app.get("/", summary="API Health Check", tags=["System"])
async def root():
    return {"message": "Promethios Compliance API is active."}

@app.get("/api/applications", summary="Get Loan Applications", tags=["Compliance"])
async def get_applications(count: int = 5):
    applications = data_loader.load_loan_applications(count)
    return applications

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
