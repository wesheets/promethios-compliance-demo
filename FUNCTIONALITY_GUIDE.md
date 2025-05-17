# Promethios Compliance Demo - Phase 2 Functionality Guide

This guide provides a detailed explanation of the Phase 2 features implemented in the Promethios Compliance Demo. It covers how each component works, how they integrate with each other, and how to use them effectively.

## Table of Contents

1. [Multi-Factor Trust Evaluation Framework](#1-multi-factor-trust-evaluation-framework)
2. [Dynamic Regulatory Mapping System](#2-dynamic-regulatory-mapping-system)
3. [Role-Specific Dashboards](#3-role-specific-dashboards)
4. [OpenAI-Powered Conversational Explainability](#4-openai-powered-conversational-explainability)
5. [Lender Recommendations and Compliance Timeline](#5-lender-recommendations-and-compliance-timeline)
6. [PDF Report Generation](#6-pdf-report-generation)
7. [Lending Club API Integration](#7-lending-club-api-integration)
8. [Configuration and Environment Variables](#8-configuration-and-environment-variables)
9. [API Reference](#9-api-reference)

## 1. Multi-Factor Trust Evaluation Framework

The Multi-Factor Trust Evaluation Framework provides a comprehensive approach to evaluating the trustworthiness of loan applications across multiple dimensions.

### Key Components

- **BaseTrustFactor**: An abstract base class that defines the interface for all trust factors
- **DataQualityFactor**: Evaluates the completeness, consistency, and accuracy of loan data
- **ModelConfidenceFactor**: Assesses the confidence level of model predictions
- **RegulatoryAlignmentFactor**: Checks compliance with specific regulatory requirements
- **EthicalConsiderationsFactor**: Evaluates fairness and potential bias in decision-making
- **TrustEvaluationFramework**: Orchestrates the evaluation process across all factors

### How It Works

1. **Factor Registration**: Trust factors are registered with the framework with assigned weights
2. **Application Evaluation**: When an application is evaluated, each factor produces:
   - A numerical score (0-100)
   - Detailed explanations of the score
   - Specific areas of concern or strength
3. **Weighted Scoring**: The framework calculates a weighted average of all factor scores
4. **Trustworthiness Determination**: Applications are classified as trustworthy if they exceed a configurable threshold

### Usage Example

```python
from compliance_api.trust_factors.data_quality_factor import DataQualityFactor
from compliance_api.trust_factors.model_confidence_factor import ModelConfidenceFactor
from compliance_api.trust_factors.regulatory_alignment_factor import RegulatoryAlignmentFactor
from compliance_api.trust_factors.ethical_considerations_factor import EthicalConsiderationsFactor
from compliance_api.trust_evaluation_framework import TrustEvaluationFramework

# Create the framework
framework = TrustEvaluationFramework()

# Register factors with weights
framework.register_factor("data_quality", DataQualityFactor(), weight=0.25)
framework.register_factor("model_confidence", ModelConfidenceFactor(), weight=0.25)
framework.register_factor("regulatory_alignment", RegulatoryAlignmentFactor(), weight=0.25)
framework.register_factor("ethical_considerations", EthicalConsiderationsFactor(), weight=0.25)

# Evaluate an application
application_data = {
    "application_id": "LC_123456",
    "amount": 10000,
    "purpose": "debt_consolidation",
    "grade": "A",
    # ... other application fields
}

result = framework.evaluate_application(application_data)

# Access the results
overall_score = result["overall_score"]
is_trustworthy = result["is_trustworthy"]
factor_scores = result["factors"]
```

## 2. Dynamic Regulatory Mapping System

The Dynamic Regulatory Mapping System maps trust factors to specific regulatory requirements for different frameworks, enabling detailed compliance evaluation.

### Key Components

- **RegulatoryFramework**: An abstract base class for all regulatory frameworks
- **EUAIActFramework**: Implementation of the European Union's AI Act requirements
- **FINRAFramework**: Implementation of Financial Industry Regulatory Authority requirements
- **RegulatoryMappingRegistry**: Manages multiple regulatory frameworks and their requirements

### How It Works

1. **Framework Registration**: Regulatory frameworks are registered with the registry
2. **Requirement Mapping**: Each framework defines specific requirements and how they map to trust factors
3. **Compliance Evaluation**: Applications are evaluated against specific frameworks:
   - Trust factors are evaluated first
   - Framework-specific rules are applied to determine compliance
   - Detailed compliance reports are generated with specific requirement status
4. **Multi-Framework Evaluation**: Applications can be evaluated against multiple frameworks simultaneously

### Usage Example

```python
from compliance_api.regulatory_frameworks.eu_ai_act_framework import EUAIActFramework
from compliance_api.regulatory_frameworks.finra_framework import FINRAFramework
from compliance_api.regulatory_mapping_registry import RegulatoryMappingRegistry

# Create the registry
registry = RegulatoryMappingRegistry()

# Register frameworks
registry.register_framework("EU_AI_ACT", EUAIActFramework())
registry.register_framework("FINRA", FINRAFramework())

# Get requirements for a specific framework
eu_requirements = registry.get_requirements("EU_AI_ACT")

# Evaluate compliance against a specific framework
application_data = {
    "application_id": "LC_123456",
    "amount": 10000,
    # ... other application fields
}

trust_factors = trust_framework.evaluate_application(application_data)
compliance_result = registry.evaluate_compliance("EU_AI_ACT", application_data, trust_factors)

# Access the results
is_compliant = compliance_result["is_compliant"]
compliance_score = compliance_result["compliance_score"]
reason = compliance_result["reason"]
details = compliance_result["details"]
requirements = compliance_result["requirements"]

# Evaluate against all frameworks
all_results = registry.evaluate_all_frameworks(application_data, trust_factors)
```

## 3. Role-Specific Dashboards

The Role-Specific Dashboards provide tailored views for different user roles, focusing on the information and actions most relevant to each role.

### Available Dashboards

1. **Compliance Officer Dashboard** (`/compliance-officer`)
   - Focus on regulatory compliance status
   - Detailed view of requirement satisfaction
   - Access to compliance history and audit trail
   - Tools for remediation tracking

2. **Data Scientist Dashboard** (`/data-scientist`)
   - Focus on model performance and data quality
   - Detailed trust factor scores and trends
   - Feature importance visualization
   - Tools for model monitoring and improvement

3. **Executive Dashboard** (`/executive`)
   - High-level compliance overview
   - Key metrics and trends
   - Risk assessment summary
   - Strategic recommendations

### How It Works

1. **Role Selection**: Users select their role at login or via the navigation menu
2. **Tailored Views**: Each dashboard presents information specific to the role:
   - Different visualizations and metrics
   - Role-appropriate actions and tools
   - Customized explanations and recommendations
3. **Common Data**: All dashboards access the same underlying data but present it differently
4. **Role-Based Access Control**: Certain actions may be restricted based on user role

### Usage

1. Navigate to the appropriate dashboard URL:
   - Compliance Officer: `/compliance-officer`
   - Data Scientist: `/data-scientist`
   - Executive: `/executive`

2. Each dashboard provides:
   - A summary section with key metrics
   - Detailed views for specific applications
   - Tools for analysis and action
   - Export and reporting capabilities

## 4. OpenAI-Powered Conversational Explainability

The OpenAI-Powered Conversational Explainability feature provides natural language explanations of compliance decisions and allows users to ask follow-up questions.

### Key Components

- **OpenAIExplainer**: Integrates with OpenAI's API to generate explanations and answer questions
- **Conversation Context Management**: Tracks conversation history for coherent multi-turn interactions
- **Recommendation Generator**: Creates actionable recommendations based on compliance results

### How It Works

1. **Decision Explanation**: When a compliance decision is made, the system generates a natural language explanation:
   - Summarizes the overall decision
   - Explains the key factors that influenced the decision
   - Highlights specific requirements that were met or not met

2. **Interactive Q&A**: Users can ask follow-up questions about the decision:
   - "Why was this application non-compliant?"
   - "What specific data quality issues were found?"
   - "How can we improve the compliance score?"

3. **Recommendation Generation**: The system generates specific recommendations for improvement:
   - Prioritized action items
   - Expected impact of each recommendation
   - References to specific regulatory requirements

### Usage Example

```python
from compliance_api.openai_explainer import OpenAIExplainer

# Create the explainer
explainer = OpenAIExplainer()

# Generate an explanation for a decision
decision_data = {
    "decision_id": "decision_123",
    "application_id": "app_456",
    "is_compliant": False,
    "compliance_score": 65.0,
    "framework": "EU_AI_ACT",
    "primary_reason": "Insufficient data quality",
    "trust_factors": {
        # ... trust factor details
    },
    "requirements": [
        # ... requirement details
    ]
}

explanation = explainer.explain_decision(decision_data)

# Ask a follow-up question
query = "What specific data quality issues were found?"
answer = explainer.explain_decision(decision_data, query)

# Generate recommendations
application_data = {"application_id": "app_456"}
trust_factors = decision_data["trust_factors"]
recommendations = explainer.generate_recommendations(application_data, trust_factors)
```

## 5. Lender Recommendations and Compliance Timeline

This feature provides actionable recommendations for lenders and tracks the compliance history of applications over time.

### Key Components

- **ComplianceTimeline**: Tracks the history of compliance evaluations and remediation actions
- **Recommendation Engine**: Generates specific recommendations for improving compliance
- **Trend Analysis**: Analyzes compliance score trends over time

### How It Works

1. **Event Tracking**: The system records events in the compliance timeline:
   - Evaluation events: When an application is evaluated against a regulatory framework
   - Remediation events: When actions are taken to address compliance issues
   - Verification events: When compliance is verified by a human reviewer

2. **Timeline Visualization**: Users can view the complete history of an application:
   - Chronological list of all events
   - Compliance score trends over time
   - Trust factor score trends over time

3. **Recommendation Generation**: Based on the timeline and current status, the system generates recommendations:
   - Specific actions to improve compliance
   - Prioritized by impact and urgency
   - Linked to specific regulatory requirements

### Usage Example

```python
from compliance_api.compliance_timeline import ComplianceTimeline

# Create the timeline
timeline = ComplianceTimeline()

# Add an evaluation event
evaluation_event = timeline.add_event(
    application_id="app_123",
    event_type="evaluation",
    event_data={
        "is_compliant": False,
        "compliance_score": 65.0,
        "framework": "EU_AI_ACT",
        "primary_reason": "Insufficient data quality"
    }
)

# Add a remediation event
remediation_event = timeline.add_event(
    application_id="app_123",
    event_type="remediation",
    event_data={
        "action": "Improve data quality",
        "description": "Verified employment information and resolved income data inconsistencies",
        "impact": "Data quality score improved from 60.0 to 85.0"
    }
)

# Get the complete timeline
events = timeline.get_timeline("app_123")

# Get compliance history
compliance_history = timeline.get_compliance_history("app_123")

# Get compliance trend
trend = timeline.get_compliance_trend("app_123")
```

## 6. PDF Report Generation

The PDF Report Generation feature creates comprehensive compliance reports that can be downloaded, shared, and archived.

### Key Components

- **ComplianceReportGenerator**: Creates PDF reports with detailed compliance information
- **Visualization Components**: Generates charts and graphs for the reports
- **Base64 Encoding**: Allows reports to be easily embedded in web pages or emails

### How It Works

1. **Report Generation**: When a user requests a report, the system:
   - Gathers all relevant compliance data
   - Formats it into a structured document
   - Generates visualizations for key metrics
   - Creates a professional PDF document

2. **Report Content**:
   - Executive summary with key metrics
   - Detailed compliance status for each requirement
   - Trust factor scores and explanations
   - Recommendations for improvement
   - Compliance history and trends
   - Appendices with detailed data

3. **Distribution Options**:
   - Download as PDF
   - Email to stakeholders
   - Store in document management system
   - Print for physical records

### Usage Example

```python
from compliance_api.pdf_report_generator import ComplianceReportGenerator

# Create the generator
generator = ComplianceReportGenerator()

# Generate a report
decision_data = {
    "decision_id": "decision_123",
    "application_id": "app_456",
    "is_compliant": False,
    "compliance_score": 65.0,
    "framework": "EU_AI_ACT",
    "primary_reason": "Insufficient data quality",
    # ... other decision data
}

trust_factors = {
    "overall_score": 70.0,
    "factors": {
        "data_quality": {"score": 60.0},
        "model_confidence": {"score": 75.0},
        "regulatory_alignment": {"score": 65.0},
        "ethical_considerations": {"score": 80.0}
    }
}

recommendations = [
    {
        "title": "Improve Data Quality",
        "description": "Verify employment information and resolve inconsistencies in income data.",
        "priority": "high"
    },
    # ... other recommendations
]

# Generate the PDF
pdf_data = generator.generate_report(decision_data, trust_factors, recommendations)

# Save to file
with open("compliance_report.pdf", "wb") as f:
    f.write(pdf_data)

# Convert to base64 for embedding in web pages
base64_data = generator.encode_pdf_to_base64(pdf_data)
```

## 7. Lending Club API Integration

The Lending Club API Integration connects the system to real loan data from Lending Club, enabling compliance evaluation of actual loan applications.

### Key Components

- **LendingClubAPI**: Connects to the Lending Club API and retrieves loan data
- **Data Transformation**: Maps Lending Club data to the format expected by the compliance system
- **Mock Data Generator**: Provides realistic test data when the API is not available

### How It Works

1. **API Connection**: The system connects to the Lending Club API using authentication credentials
2. **Data Retrieval**: Loan application data is retrieved from Lending Club:
   - Available loans can be listed and filtered
   - Detailed information for specific loans can be retrieved
3. **Data Transformation**: Lending Club data is transformed to the internal format:
   - Field names are standardized
   - Data types are converted as needed
   - Missing fields are handled gracefully
4. **Compliance Evaluation**: The transformed data is passed to the compliance evaluation system

### Usage Example

```python
from compliance_api.lending_club_api import LendingClubAPI

# Create the API client
api = LendingClubAPI()

# Get available loans
loans = api.get_available_loans(limit=10)

# Get details for a specific loan
loan = api.get_loan_details("123456")

# Generate mock data for testing
mock_loans = api.mock_loan_data(count=5)

# Use the loan data for compliance evaluation
for loan in loans:
    trust_result = trust_framework.evaluate_application(loan)
    compliance_result = registry.evaluate_compliance("EU_AI_ACT", loan, trust_result)
    # ... process the results
```

## 8. Configuration and Environment Variables

The system requires several environment variables for proper operation in production:

### Required Environment Variables

- **OPENAI_API_KEY**: API key for OpenAI (required for conversational explainability)
- **LENDING_CLUB_API_KEY**: API key for Lending Club (required for API integration)
- **FLASK_SECRET_KEY**: Secret key for Flask session security
- **DATABASE_URL**: Connection string for the database (if using persistent storage)

### Optional Environment Variables

- **LOG_LEVEL**: Logging level (default: INFO)
- **PORT**: Port for the web server (default: 5000)
- **TRUST_THRESHOLD**: Default threshold for trustworthiness (default: 80.0)
- **COMPLIANCE_THRESHOLD**: Default threshold for compliance (default: 80.0)
- **STORAGE_PATH**: Path for persistent storage of timelines (default: in-memory)

### Configuration in Production

For production deployment on Render, set these environment variables in the Render dashboard:

1. Go to the Render dashboard
2. Select your service
3. Go to the "Environment" tab
4. Add each required environment variable
5. Click "Save Changes"

## 9. API Reference

The system provides several API endpoints for integration with other systems:

### Trust Evaluation API

- **GET /api/trust-factors**: List available trust factors
- **POST /api/evaluate-trust**: Evaluate an application using the trust framework
  - Request body: Application data
  - Response: Trust evaluation result with factor scores

### Regulatory Compliance API

- **GET /api/frameworks**: List available regulatory frameworks
- **GET /api/frameworks/{framework}/requirements**: List requirements for a specific framework
- **POST /api/evaluate-compliance**: Evaluate compliance against a specific framework
  - Request body: Application data and framework ID
  - Response: Compliance evaluation result with requirement status

### Timeline API

- **GET /api/timeline/{application_id}**: Get the complete timeline for an application
- **GET /api/timeline/{application_id}/compliance**: Get compliance history for an application
- **GET /api/timeline/{application_id}/trends**: Get compliance score trends for an application
- **POST /api/timeline/{application_id}/event**: Add an event to the timeline
  - Request body: Event type and data
  - Response: Created event

### Explanation API

- **POST /api/explain**: Get an explanation for a compliance decision
  - Request body: Decision data and optional query
  - Response: Natural language explanation
- **POST /api/recommendations**: Get recommendations for improving compliance
  - Request body: Application data and trust factors
  - Response: List of prioritized recommendations

### Report API

- **POST /api/generate-report**: Generate a PDF compliance report
  - Request body: Decision data, trust factors, and recommendations
  - Response: Base64-encoded PDF data

### Lending Club API

- **GET /api/loans**: Get available loans from Lending Club
  - Query parameters: limit, offset, filters
  - Response: List of transformed loan applications
- **GET /api/loans/{loan_id}**: Get details for a specific loan
  - Response: Transformed loan application data
