"""
Model Confidence Factor for the Multi-Factor Trust Evaluation Framework.

This module implements the model confidence evaluation factor, which assesses
prediction certainty and model robustness for loan applications.
"""

from .base_factor import BaseTrustFactor

class PredictionCertaintyEvaluator:
    """Evaluates the certainty of model predictions."""
    
    def evaluate(self, data):
        """
        Evaluate prediction certainty.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # For demo purposes, we'll use a simplified approach to prediction certainty
        # In a real system, this would use model confidence scores or prediction probabilities
        
        # Start with a base certainty score
        certainty_score = 70
        
        # Adjust based on loan characteristics that might affect prediction certainty
        
        # Grade affects certainty (A and B grades are more predictable)
        grade = data.get("grade", "")
        if grade in ["A", "B"]:
            certainty_score += 15
        elif grade in ["D", "E"]:
            certainty_score -= 10
        
        # Extreme values in key metrics reduce certainty
        dti = data.get("dti", 0)
        if dti > 35:
            certainty_score -= 15
        
        loan_amount = data.get("loan_amount", 0)
        if loan_amount > 35000:
            certainty_score -= 10
        
        # Employment length increases certainty (more history = more predictable)
        employment_length = data.get("employment_length", 0)
        if employment_length > 5:
            certainty_score += 10
        elif employment_length < 1:
            certainty_score -= 15
        
        # Ensure score is between 0 and 100
        return max(0, min(100, certainty_score))

class ModelRobustnessEvaluator:
    """Evaluates the robustness of the model for this type of application."""
    
    def evaluate(self, data):
        """
        Evaluate model robustness for this application type.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        # For demo purposes, we'll use a simplified approach to model robustness
        # In a real system, this would consider model performance metrics for similar applications
        
        # Start with a base robustness score
        robustness_score = 75
        
        # Adjust based on application characteristics that might affect model robustness
        
        # Purpose affects robustness (some purposes have more training data)
        purpose = data.get("purpose", "")
        common_purposes = ["debt_consolidation", "credit_card", "home_improvement"]
        if purpose in common_purposes:
            robustness_score += 15
        else:
            robustness_score -= 10
        
        # Home ownership affects robustness
        home_ownership = data.get("home_ownership", "")
        if home_ownership in ["MORTGAGE", "RENT"]:
            robustness_score += 10
        elif home_ownership == "OWN":
            robustness_score += 5
        else:
            robustness_score -= 10
        
        # Delinquencies affect robustness (more delinquencies = less robust predictions)
        delinq_2yrs = data.get("delinq_2yrs", 0)
        if delinq_2yrs > 2:
            robustness_score -= 15
        
        # Ensure score is between 0 and 100
        return max(0, min(100, robustness_score))

class ModelConfidenceFactor(BaseTrustFactor):
    """Evaluates the confidence in model predictions."""
    
    def __init__(self, weight=0.8):
        """
        Initialize the model confidence factor.
        
        Args:
            weight: Weight of the factor in the overall trust score (default: 0.8)
        """
        super().__init__("Model Confidence", weight)
        self.prediction_certainty_evaluator = PredictionCertaintyEvaluator()
        self.model_robustness_evaluator = ModelRobustnessEvaluator()
        
    def evaluate(self, data):
        """
        Evaluate model confidence based on prediction certainty and model robustness.
        
        Args:
            data: Dictionary containing loan application data
            
        Returns:
            float: Score between 0 and 100
        """
        certainty_score = self.prediction_certainty_evaluator.evaluate(data)
        robustness_score = self.model_robustness_evaluator.evaluate(data)
        
        # Calculate weighted average
        self.score = (certainty_score * 0.6 + 
                      robustness_score * 0.4)
        
        # Generate explanation
        self.explanation = {
            "factor": self.name,
            "score": self.score,
            "components": {
                "prediction_certainty": certainty_score,
                "model_robustness": robustness_score
            },
            "summary": f"Model confidence score is {self.score:.1f}/100, with "
                       f"{'high' if certainty_score > 70 else 'moderate' if certainty_score > 50 else 'low'} prediction certainty and "
                       f"{'high' if robustness_score > 70 else 'moderate' if robustness_score > 50 else 'low'} model robustness"
        }
        
        return self.score
