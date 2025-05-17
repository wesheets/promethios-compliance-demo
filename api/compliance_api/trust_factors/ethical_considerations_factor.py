"""
Ethical Considerations Factor for the Multi-Factor Trust Evaluation Framework.

This module implements the ethical considerations evaluation factor, which assesses
fairness and potential bias in loan applications.
"""

from .base_factor import BaseTrustFactor

class FairnessEvaluator:
    """Evaluates the fairness of loan application processing."""
    
    def evaluate(self, data):
        """
        Evaluate fairness.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # For demo purposes, we'll use a simplified approach to fairness evaluation
        # In a real system, this would use more sophisticated fairness metrics
        
        # Start with a base fairness score
        fairness_score = 80
        
        # Check if the loan terms are fair relative to the applicant's profile
        grade = data.get("grade", "")
        interest_rate = data.get("interest_rate", 0)
        dti = data.get("dti", 0)
        annual_income = data.get("annual_income", 0)
        
        # Check if interest rate is appropriate for the grade
        if grade == "A" and interest_rate > 10:
            fairness_score -= 20
        elif grade == "B" and interest_rate > 15:
            fairness_score -= 15
        elif grade == "C" and interest_rate > 20:
            fairness_score -= 10
        
        # Check if loan amount is reasonable relative to income
        loan_amount = data.get("loan_amount", 0)
        if annual_income > 0:
            loan_to_income_ratio = loan_amount / annual_income
            if loan_to_income_ratio > 1.0:
                fairness_score -= 15
            elif loan_to_income_ratio > 0.5:
                fairness_score -= 5
        
        # Check if DTI is being fairly considered
        if dti > 40 and grade in ["A", "B"]:
            fairness_score -= 15
        
        # Ensure score is between 0 and 100
        return max(0, min(100, fairness_score))

class BiasDetectionEvaluator:
    """Evaluates potential bias in loan application processing."""
    
    def evaluate(self, data):
        """
        Evaluate potential bias.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # For demo purposes, we'll use a simplified approach to bias detection
        # In a real system, this would use more sophisticated bias detection methods
        
        # Start with a perfect score (no bias detected)
        bias_score = 100
        
        # Check for potential bias indicators
        home_ownership = data.get("home_ownership", "")
        employment_length = data.get("employment_length", 0)
        purpose = data.get("purpose", "")
        
        # Check for potential home ownership bias
        if home_ownership not in ["MORTGAGE", "RENT", "OWN"]:
            bias_score -= 15
        
        # Check for potential employment length bias
        if employment_length < 2:
            bias_score -= 10
        
        # Check for potential loan purpose bias
        uncommon_purposes = ["wedding", "vacation", "moving", "medical"]
        if purpose in uncommon_purposes:
            bias_score -= 15
        
        # Ensure score is between 0 and 100
        return max(0, min(100, bias_score))

class EthicalConsiderationsFactor(BaseTrustFactor):
    """Evaluates ethical considerations in loan application processing."""
    
    def __init__(self, weight=1.0):
        """
        Initialize the ethical considerations factor.
        
        Args:
            weight: Weight of the factor in the overall trust score (default: 1.0)
        """
        super().__init__("Ethical Considerations", weight)
        self.fairness_evaluator = FairnessEvaluator()
        self.bias_detection_evaluator = BiasDetectionEvaluator()
        
    def evaluate(self, data):
        """
        Evaluate ethical considerations based on fairness and bias detection.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        fairness_score = self.fairness_evaluator.evaluate(data)
        bias_score = self.bias_detection_evaluator.evaluate(data)
        
        # Calculate weighted average
        self.score = (fairness_score * 0.6 + 
                      bias_score * 0.4)
        
        # Generate explanation
        self.explanation = {
            "factor": self.name,
            "score": self.score,
            "components": {
                "fairness": fairness_score,
                "bias_detection": bias_score
            },
            "summary": f"Ethical considerations score is {self.score:.1f}/100, with "
                       f"{'high' if fairness_score > 70 else 'moderate' if fairness_score > 50 else 'low'} fairness and "
                       f"{'minimal' if bias_score > 70 else 'moderate' if bias_score > 50 else 'significant'} potential bias"
        }
        
        return self.score
