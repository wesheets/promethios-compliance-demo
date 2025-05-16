import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ComplianceWrapper:
    def __init__(self, base_url=None):
        # Use environment variable or default
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8002")
        
    def evaluate_compliance(self, loan_application, regulatory_framework="GDPR"):
        """
        Evaluate compliance of a loan application against a regulatory framework.
        
        Args:
            loan_application: Dictionary containing loan application data
            regulatory_framework: Regulatory framework to check against (e.g., "GDPR", "FCRA")
            
        Returns:
            Dictionary with compliance results
        """
        # For demo purposes, we'll use a simple trust score calculation
        trust_score = self._calculate_trust_score(loan_application)
        
        # Check against regulatory framework
        return self._check_regulatory_compliance(trust_score, regulatory_framework)
    
    def _calculate_trust_score(self, loan_application):
        """Calculate a trust score based on loan application data."""
        # This is a simplified scoring model for demo purposes
        score = 50  # Base score
        
        # Adjust based on loan amount (higher loans = higher risk)
        loan_amount = loan_application.get("loan_amount", 0)
        if loan_amount < 10000:
            score += 15
        elif loan_amount > 30000:
            score -= 15
        
        # Adjust based on employment length (longer = more stable)
        employment_length = loan_application.get("employment_length", 0)
        if employment_length > 5:
            score += 10
        elif employment_length < 2:
            score -= 10
        
        # Adjust based on debt-to-income ratio (lower = better)
        dti = loan_application.get("dti", 0)
        if dti < 15:
            score += 15
        elif dti > 30:
            score -= 15
        
        # Adjust based on delinquencies (fewer = better)
        delinq = loan_application.get("delinq_2yrs", 0)
        if delinq == 0:
            score += 10
        elif delinq > 2:
            score -= 20
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))
    
    def _check_regulatory_compliance(self, trust_score, regulatory_framework):
        """Check if trust score meets regulatory framework requirements."""
        # Different frameworks have different thresholds
        thresholds = {
            "GDPR": 65,
            "FCRA": 60,
            "CCPA": 70,
            "GLBA": 75
        }
        
        threshold = thresholds.get(regulatory_framework, 65)  # Default to GDPR threshold
        
        if trust_score >= threshold:
            return {
                "compliant": True,
                "framework": regulatory_framework,
                "details": f"Trust score {trust_score} meets {regulatory_framework} threshold of {threshold}"
            }
        else:
            return {
                "compliant": False,
                "framework": regulatory_framework,
                "details": f"Trust score {trust_score} below {regulatory_framework} threshold of {threshold}",
                "remediation": "Escalate to human reviewer"
            }
