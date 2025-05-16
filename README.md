# Promethios Compliance Demo
AI Compliance Replay System built on the Promethios Governance Kernel.

## Overview
This repository contains a compliance-focused demo application built on top of the Promethios AI Governance Kernel. It demonstrates how Promethios can be used to create a robust compliance system for AI decision-making, with features including:
- Multi-factor trust evaluation
- Dynamic regulatory mapping
- Cryptographic verification of decision trails
- Conversational explanations of compliance status
- Business impact metrics

## Repository Structure
- `api/promethios_core/`: Core files from the Promethios Governance Kernel
- `api/compliance_api/`: Compliance API-specific code
- `web/`: Web UI for the compliance demo
- `data/`: Sample data for the demo
- `logs/`: Log files generated during operation

## Deployment
This demo is deployed on Render and can be accessed at:
- Web UI: [https://promethios-compliance-web.onrender.com](https://promethios-compliance-web.onrender.com)
- API: [https://promethios-compliance-api.onrender.com](https://promethios-compliance-api.onrender.com)

## Local Development
### Prerequisites
- Python 3.9+
- pip

### Setup
1. Clone this repository
```bash
git clone https://github.com/your-username/promethios-compliance-demo.git
cd promethios-compliance-demo
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# For API
cd api
cp .env.example .env
# Edit .env as needed

# For Web
cd ../web
cp .env.example .env
# Edit .env as needed
```

4. Start the API
```bash
cd api
python promethios_api.py
```

5. In another terminal, start the web UI
```bash
cd web
python app.py
```

6. Access the demo UI at http://localhost:5002

## Deployment to Render
This repository includes a render.yaml file for easy deployment to Render.

1. Fork this repository to your GitHub account
2. Sign up for a Render account at https://render.com
3. Connect your GitHub account to Render
4. Create a new Blueprint on Render and select this repository
5. Render will automatically deploy both the API and web UI services

## Development Roadmap
This demo is being developed in phases:
1. Core Compliance Wrapper (Days 1-3)
2. Enhanced Trust Factors & Regulatory Mapping (Days 4-7)
3. Replay and Verification Features (Days 8-10)
4. Business Impact Metrics and Final Polish (Days 11-12)

Each phase ends with a working demo that builds upon the previous phase.
