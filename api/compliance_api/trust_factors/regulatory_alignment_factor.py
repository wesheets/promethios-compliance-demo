"""
Regulatory Alignment Factor for the Multi-Factor Trust Evaluation Framework.

This module implements the regulatory alignment evaluation factor, which assesses
how well a loan application aligns with specific regulatory requirements.
"""

from .base_factor import BaseTrustFactor

class FrameworkComplianceEvaluator:
    """Evaluates compliance with specific regulatory frameworks."""
    
    def evaluate(self, data):
        """
        Evaluate framework compliance.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # Get the regulatory framework to check against
        framework = data.get("regulatory_framework", "EU_AI_ACT")
        
        # Start with a base compliance score
        compliance_score = 70
        
        # Adjust based on framework-specific requirements
        if framework == "EU_AI_ACT":
            # EU AI Act emphasizes transparency and fairness
            grade = data.get("grade", "")
            dti = data.get("dti", 0)
            
            # Grade A and B loans are generally more transparent in their risk assessment
            if grade in ["A", "B"]:
                compliance_score += 15
            elif grade in ["D", "E"]:
                compliance_score -= 10
            
            # Lower DTI ratios are more likely to be fair assessments
            if dti < 20:
                compliance_score += 10
            elif dti > 35:
                compliance_score -= 15
                
        elif framework == "FINRA":
            # FINRA emphasizes proper risk assessment and disclosure
            delinq_2yrs = data.get("delinq_2yrs", 0)
            dti = data.get("dti", 0)
            
            # Fewer delinquencies indicate better risk assessment
            if delinq_2yrs == 0:
                compliance_score += 15
            elif delinq_2yrs > 2:
                compliance_score -= 20
            
            # Lower DTI ratios are less risky
            if dti < 25:
                compliance_score += 10
            elif dti > 40:
                compliance_score -= 15
                
        elif framework == "GDPR":
            # GDPR emphasizes data protection and consent
            # For demo purposes, we'll assume all applications have proper consent
            compliance_score += 10
            
        # Ensure score is between 0 and 100
        return max(0, min(100, compliance_score))

class DocumentationEvaluator:
    """Evaluates the quality and completeness of documentation."""
    
    def evaluate(self, data):
        """
        Evaluate documentation quality.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # For demo purposes, we'll use a simplified approach to documentation evaluation
        # In a real system, this would check for presence of required documentation
        
        # Start with a base documentation score
        documentation_score = 65
        
        # Adjust based on application completeness as a proxy for documentation
        # Required fields for a complete loan application
        required_fields = [
            "id", "loan_amount", "interest_rate", "grade", 
            "employment_length", "home_ownership", "annual_income", 
            "purpose", "dti", "delinq_2yrs"
        ]
        
        # Count how many required fields are present and have non-empty values
        present_fields = sum(1 for field in required_fields if field in data and data[field] is not None)
        
        # Calculate completeness percentage
        completeness = (present_fields / len(required_fields))
        
        # Adjust documentation score based on completeness
        if completeness > 0.9:
            documentation_score += 25
        elif completeness > 0.7:
            documentation_score += 15
        elif completeness < 0.5:
            documentation_score -= 20
        
        # Ensure score is between 0 and 100
        return max(0, min(100, documentation_score))

class RegulatoryAlignmentFactor(BaseTrustFactor):
    """Evaluates alignment with regulatory requirements."""
    
    def __init__(self, weight=1.2):
        """
        Initialize the regulatory alignment factor.
        
        Args:
            weight: Weight of the factor in the overall trust score (default: 1.2)
        """
        super().__init__("Regulatory Alignment", weight)
        self.framework_compliance_evaluator = FrameworkComplianceEvaluator()
        self.documentation_evaluator = DocumentationEvaluator()
        
    def evaluate(self, data):
        """
        Evaluate regulatory alignment based on framework compliance and documentation.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        framework_score = self.framework_compliance_evaluator.evaluate(data)
        documentation_score = self.documentation_evaluator.evaluate(data)
        
        # Calculate weighted average
        self.score = (framework_score * 0.7 + 
                      documentation_score * 0.3)
        
        # Get the regulatory framework name for the explanation
        framework = data.get("regulatory_framework", "EU_AI_ACT")
        
        # Generate explanation
        self.explanation = {
            "factor": self.name,
            "score": self.score,
            "components": {
                "framework_compliance": framework_score,
                "documentation": documentation_score
            },
            "summary": f"Regulatory alignment score is {self.score:.1f}/100 for {framework}, with "
                       f"{'strong' if framework_score > 70 else 'moderate' if framework_score > 50 else 'weak'} framework compliance and "
                       f"{'thorough' if documentation_score > 70 else 'adequate' if documentation_score > 50 else 'insufficient'} documentation"
        }
        
        return self.score
