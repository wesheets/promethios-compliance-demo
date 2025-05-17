"""
Data Quality Factor for the Multi-Factor Trust Evaluation Framework.

This module implements the data quality evaluation factor, which assesses
completeness, consistency, and accuracy of loan application data.
"""

from .base_factor import BaseTrustFactor

class CompletenessEvaluator:
    """Evaluates the completeness of data."""
    
    def evaluate(self, data):
        """
        Evaluate data completeness.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # Required fields for a complete loan application
        required_fields = [
            "id", "loan_amount", "interest_rate", "grade", 
            "employment_length", "home_ownership", "annual_income", 
            "purpose", "dti", "delinq_2yrs"
        ]
        
        # Count how many required fields are present and have non-empty values
        present_fields = sum(1 for field in required_fields if field in data and data[field] is not None)
        
        # Calculate completeness score
        completeness_score = (present_fields / len(required_fields)) * 100
        
        return completeness_score

class ConsistencyEvaluator:
    """Evaluates the consistency of data."""
    
    def evaluate(self, data):
        """
        Evaluate data consistency.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # Start with perfect score and deduct for inconsistencies
        consistency_score = 100
        
        # Check if loan amount is consistent with grade (higher grades should have lower amounts)
        loan_amount = data.get("loan_amount", 0)
        grade = data.get("grade", "")
        
        if grade == "A" and loan_amount > 30000:
            consistency_score -= 20
        elif grade == "E" and loan_amount < 5000:
            consistency_score -= 20
        
        # Check if DTI is consistent with annual income and loan amount
        dti = data.get("dti", 0)
        annual_income = data.get("annual_income", 0)
        
        if annual_income > 0:
            # Calculate expected DTI based on loan amount and income
            expected_dti = (loan_amount / annual_income) * 100
            
            # If actual DTI differs significantly from expected, deduct points
            if abs(dti - expected_dti) > 20:
                consistency_score -= 30
        
        # Ensure score is between 0 and 100
        return max(0, min(100, consistency_score))

class AccuracyEvaluator:
    """Evaluates the accuracy of data."""
    
    def evaluate(self, data):
        """
        Evaluate data accuracy.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # Start with perfect score and deduct for potential inaccuracies
        accuracy_score = 100
        
        # Check if values are within reasonable ranges
        loan_amount = data.get("loan_amount", 0)
        interest_rate = data.get("interest_rate", 0)
        annual_income = data.get("annual_income", 0)
        dti = data.get("dti", 0)
        
        # Check loan amount range
        if loan_amount <= 0 or loan_amount > 100000:
            accuracy_score -= 20
        
        # Check interest rate range
        if interest_rate <= 0 or interest_rate > 30:
            accuracy_score -= 20
        
        # Check annual income range
        if annual_income <= 0 or annual_income > 500000:
            accuracy_score -= 20
        
        # Check DTI range
        if dti <= 0 or dti > 100:
            accuracy_score -= 20
        
        # Ensure score is between 0 and 100
        return max(0, min(100, accuracy_score))

class DataQualityFactor(BaseTrustFactor):
    """Evaluates the quality of input data."""
    
    def __init__(self, weight=1.0):
        """
        Initialize the data quality factor.
        
        Args:
            weight: Weight of the factor in the overall trust score (default: 1.0)
        """
        super().__init__("Data Quality", weight)
        self.completeness_evaluator = CompletenessEvaluator()
        self.consistency_evaluator = ConsistencyEvaluator()
        self.accuracy_evaluator = AccuracyEvaluator()
        
    def evaluate(self, data):
        """
        Evaluate data quality based on completeness, consistency, and accuracy.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        completeness_score = self.completeness_evaluator.evaluate(data)
        consistency_score = self.consistency_evaluator.evaluate(data)
        accuracy_score = self.accuracy_evaluator.evaluate(data)
        
        # Calculate weighted average
        self.score = (completeness_score * 0.4 + 
                      consistency_score * 0.3 + 
                      accuracy_score * 0.3)
        
        # Generate explanation
        self.explanation = {
            "factor": self.name,
            "score": self.score,
            "components": {
                "completeness": completeness_score,
                "consistency": consistency_score,
                "accuracy": accuracy_score
            },
            "summary": f"Data quality score is {self.score:.1f}/100, with strengths in "
                       f"{'completeness' if completeness_score > 70 else 'consistency' if consistency_score > 70 else 'accuracy'}"
        }
        
        return self.score
