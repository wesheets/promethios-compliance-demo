# Promethios Compliance Demo

## Overview

The Promethios Compliance Demo is an interactive web application that demonstrates AI governance and regulatory compliance for financial loan applications. It showcases how organizations can evaluate loan applications against various regulatory frameworks, ensure compliance with industry standards, and provide transparent explanations for compliance decisions.

This demo implements a comprehensive trust evaluation framework that assesses applications across multiple dimensions, maps them to specific regulatory requirements, and provides detailed explanations and recommendations.

## Features

### Multi-Factor Trust Evaluation Framework

The core of the system is a modular trust evaluation framework that assesses loan applications across multiple dimensions:

- **Data Quality**: Evaluates the completeness, consistency, and accuracy of loan data
- **Model Confidence**: Assesses the confidence level and robustness of model predictions
- **Regulatory Alignment**: Checks compliance with specific regulatory requirements
- **Ethical Considerations**: Evaluates fairness and potential bias in decision-making

Each factor produces a numerical score and detailed explanations, which are combined into an overall trust score using configurable weights.

### Dynamic Regulatory Mapping System

The system maps trust factors to specific regulatory requirements for different frameworks:

- **EU AI Act**: European Union's Artificial Intelligence Act requirements
- **FINRA**: Financial Industry Regulatory Authority requirements
- **Internal**: Organization-specific compliance policies

Each framework defines specific requirements and how they map to trust factors, enabling detailed compliance evaluation against multiple regulatory standards simultaneously.

### Role-Specific Dashboards

The application provides specialized dashboards for different user roles:

#### Compliance Officer Dashboard

- Focus on regulatory compliance status
- Detailed view of requirement satisfaction
- Access to compliance history and audit trail
- Tools for remediation tracking

#### Data Scientist Dashboard

- Focus on model performance and data quality
- Detailed trust factor scores and trends
- Feature importance visualization
- Tools for model monitoring and improvement

#### Executive Dashboard

- High-level compliance overview
- Key metrics and trends
- Risk assessment summary
- Strategic recommendations

### OpenAI-Powered Conversational Explainability

The system provides natural language explanations of compliance decisions:

- Detailed explanations of why an application is compliant or non-compliant
- Interactive Q&A about specific aspects of the decision
- Personalized recommendations for improving compliance
- Context-aware responses that maintain conversation history

### Backend Analysis Logging

The system includes a real-time backend analysis logging panel that demonstrates the detailed processing happening behind the scenes:

- **Color-coded log entries** for different analysis types:
  - Green: Data Quality Analysis
  - Blue: Model Confidence Analysis
  - Orange: Regulatory Alignment Analysis
  - Purple: Ethical Considerations Analysis
  - Red: Compliance Decisions
- **Real-time updates** with auto-refresh capability
- **Filtering options** to focus on specific analysis types
- **Detailed JSON data** showing exact scores and metrics for each analysis step
- **Timestamp tracking** to monitor processing sequence

This feature provides transparency into the AI governance process, showing exactly how decisions are made even when using sample data.

### Lender Recommendations and Compliance Timeline

The system tracks the compliance history of applications over time:

- Chronological timeline of all compliance evaluations
- Record of remediation actions and their impact
- Compliance score trends over time
- Actionable recommendations for improving compliance

### PDF Report Generation

The system can generate comprehensive compliance reports:

- Executive summary with key metrics
- Detailed compliance status for each requirement
- Trust factor scores and explanations
- Recommendations for improvement
- Compliance history and trends

### Lending Club API Integration

The system can connect to real loan data from Lending Club:

- Retrieval of available loans
- Transformation of Lending Club data to internal format
- Compliance evaluation of actual loan applications
- Mock data generation for testing

## Pages and Navigation

### Home Page

The home page provides an overview of the system and access to all features:

- **Navigation Bar**: Access to all dashboards and help information
- **Loan Applications**: List of available loan applications with details
- **Compliance Results**: View compliance evaluation results
- **Processed Decisions**: History of all processed decisions
- **Backend Analysis Logs**: Real-time display of backend processing steps

### Compliance Officer Dashboard

Accessed via `/compliance-officer`, this dashboard focuses on regulatory compliance:

- **Compliance Status**: Overview of compliance status across all applications
- **Requirement Details**: Detailed view of requirement satisfaction
- **Remediation Tracking**: Tools for tracking remediation actions
- **Audit Trail**: Complete history of compliance evaluations

### Data Scientist Dashboard

Accessed via `/data-scientist`, this dashboard focuses on model performance:

- **Trust Factor Analysis**: Detailed view of trust factor scores
- **Data Quality Metrics**: Metrics on data completeness and accuracy
- **Model Performance**: Confidence scores and prediction accuracy
- **Feature Importance**: Visualization of feature importance

### Executive Dashboard

Accessed via `/executive`, this dashboard provides a high-level overview:

- **Compliance Summary**: High-level overview of compliance status
- **Risk Assessment**: Identification of high-risk areas
- **Trend Analysis**: Compliance trends over time
- **Strategic Recommendations**: Actionable insights for improvement

## How It Works

### Compliance Evaluation Process

1. **Application Selection**: User selects a loan application to evaluate
2. **Framework Selection**: User selects a regulatory framework (EU AI Act, FINRA, Internal)
3. **Trust Evaluation**: The system evaluates the application across multiple trust factors
4. **Regulatory Mapping**: Trust factors are mapped to specific regulatory requirements
5. **Compliance Determination**: The system determines if the application is compliant
6. **Explanation Generation**: The system generates natural language explanations
7. **Recommendation Generation**: The system provides actionable recommendations
8. **Real-time Logging**: All analysis steps are logged and displayed in the logging panel

### Technical Architecture

The system is built using a modern web architecture:

- **Frontend**: HTML, CSS, JavaScript with Bootstrap for responsive design
- **Backend**: Python with Flask for the web server and FastAPI for the API
- **Database**: In-memory storage with optional persistence
- **External Integrations**: OpenAI API for explanations, Lending Club API for loan data
- **Logging System**: Thread-safe logging with real-time frontend display

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for conversational explainability)
- Lending Club API key (optional, for real loan data)

### Configuration

Set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LENDING_CLUB_API_KEY`: Your Lending Club API key (optional)
- `FLASK_SECRET_KEY`: Secret key for Flask session security

### Running Locally

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run the API: `python api/promethios_api.py`
5. Run the web server: `python web/app.py`
6. Access the application at `http://localhost:5000`

### Deployment

The application is deployed on Render:

- Web UI: https://promethios-compliance-web.onrender.com
- API: https://promethios-compliance-api.onrender.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
