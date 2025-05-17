"""
Base Trust Factor for the Multi-Factor Trust Evaluation Framework.

This module defines the abstract base class for all trust factors used in
evaluating compliance decisions.
"""

class BaseTrustFactor:
    """Base class for all trust factors."""
    
    def __init__(self, name, weight=1.0):
        """
        Initialize a trust factor.
        
        Args:
            name: Name of the trust factor
            weight: Weight of the factor in the overall trust score (default: 1.0)
        """
        self.name = name
        self.weight = weight
        self.score = None
        self.explanation = None
        
    def evaluate(self, data):
        """
        Evaluate the trust factor based on input data.
        Must be implemented by subclasses.
        
        Args:
            data: Dictionary containing relevant data for evaluation
            
        Returns:
            float: Score between 0 and 100
        """
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def get_score(self):
        """
        Get the calculated score.
        
        Returns:
            float: Score between 0 and 100
        
        Raises:
            ValueError: If factor has not been evaluated yet
        """
        if self.score is None:
            raise ValueError("Factor has not been evaluated yet")
        return self.score
    
    def get_explanation(self):
        """
        Get explanation for the score.
        
        Returns:
            dict: Explanation data with factor name, score, and details
        
        Raises:
            ValueError: If factor has not been evaluated yet
        """
        if self.explanation is None:
            raise ValueError("Factor has not been evaluated yet")
        return self.explanation
