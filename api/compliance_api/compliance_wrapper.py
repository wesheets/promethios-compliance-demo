import requests
import json
import os
from dotenv import load_dotenv
from .trust_evaluation_framework import TrustEvaluationFramework

# Load environment variables
load_dotenv()

class ComplianceWrapper:
    def __init__(self, base_url=None):
        # Use environment variable or default
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8002")
        # Initialize the trust evaluation framework
        self.trust_framework = TrustEvaluationFramework()
        
    def evaluate_compliance(self, loan_application, regulatory_framework="EU_AI_ACT"):
        """
        Evaluate compliance of a loan application against a regulatory framework.
        
        Args:
            loan_application: Dictionary containing loan application data
            regulatory_framework: Regulatory framework to check against (e.g., "EU_AI_ACT", "FINRA")
            
        Returns:
            Dictionary with compliance results
        """
        # Use the multi-factor trust evaluation framework
        evaluation_results = self.trust_framework.evaluate(loan_application, regulatory_framework)
        
        # Extract key information for the response
        overall_score = evaluation_results["overall_score"]
        is_compliant = evaluation_results["compliant"]
        
        # Prepare the response
        response = {
            "compliant": is_compliant,
            "framework": regulatory_framework,
            "overall_score": overall_score,
            "factors": {}
        }
        
        # Add factor details
        for factor_id, factor_data in evaluation_results["factors"].items():
            response["factors"][factor_id] = {
                "score": factor_data["score"],
                "summary": factor_data["explanation"]["summary"]
            }
        
        # Add details and remediation
        if is_compliant:
            response["details"] = f"Trust score {overall_score:.1f} meets {regulatory_framework} threshold"
        else:
            response["details"] = f"Trust score {overall_score:.1f} below {regulatory_framework} threshold"
            
            # Identify the lowest scoring factor for remediation
            lowest_factor = min(
                evaluation_results["factors"].items(),
                key=lambda x: x[1]["score"]
            )
            factor_id, factor_data = lowest_factor
            
            response["remediation"] = f"Improve {factor_data['explanation']['factor']} score: {factor_data['explanation']['summary']}"
        
        return response
    
    # Legacy methods kept for backward compatibility
    def _calculate_trust_score(self, loan_application):
        """Legacy method for calculating a trust score based on loan application data."""
        # Use the new framework but return just the overall score
        evaluation_results = self.trust_framework.evaluate(loan_application)
        return evaluation_results["overall_score"]
    
    def _check_regulatory_compliance(self, trust_score, regulatory_framework):
        """Legacy method to check if trust score meets regulatory framework requirements."""
        # Different frameworks have different thresholds
        thresholds = {
            "GDPR": 65,
            "FCRA": 60,
            "CCPA": 70,
            "GLBA": 75,
            "EU_AI_ACT": 80,
            "FINRA": 70
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
