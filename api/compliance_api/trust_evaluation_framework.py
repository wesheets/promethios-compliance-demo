"""
Trust Evaluation Framework for the Multi-Factor Trust Evaluation.

This module implements the framework that manages multiple trust factors
and calculates an overall trust score for compliance decisions.
"""

from .trust_factors import (
    DataQualityFactor,
    ModelConfidenceFactor,
    RegulatoryAlignmentFactor,
    EthicalConsiderationsFactor
)

class TrustEvaluationFramework:
    """Framework for evaluating trust using multiple factors."""
    
    def __init__(self):
        """Initialize the trust evaluation framework with default factors."""
        self.factors = {
            "data_quality": DataQualityFactor(weight=1.0),
            "model_confidence": ModelConfidenceFactor(weight=0.8),
            "regulatory_alignment": RegulatoryAlignmentFactor(weight=1.2),
            "ethical_considerations": EthicalConsiderationsFactor(weight=1.0)
        }
        self.results = None
        
    def evaluate(self, data, regulatory_framework="EU_AI_ACT"):
        """
        Evaluate all trust factors for the given data.
        
        Args:
            data: Dictionary containing loan application data
            regulatory_framework: Regulatory framework to check against
            
        Returns:
            dict: Evaluation results with scores and explanations
        """
        # Add regulatory framework to data
        data["regulatory_framework"] = regulatory_framework
        
        # Evaluate each factor
        factor_results = {}
        weighted_sum = 0
        total_weight = 0
        
        for factor_id, factor in self.factors.items():
            score = factor.evaluate(data)
            factor_results[factor_id] = {
                "score": score,
                "weight": factor.weight,
                "explanation": factor.get_explanation()
            }
            weighted_sum += score * factor.weight
            total_weight += factor.weight
        
        # Calculate overall trust score
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Store results
        self.results = {
            "overall_score": overall_score,
            "regulatory_framework": regulatory_framework,
            "factors": factor_results,
            "compliant": overall_score >= self._get_threshold(regulatory_framework)
        }
        
        return self.results
    
    def _get_threshold(self, regulatory_framework):
        """Get compliance threshold for the given regulatory framework."""
        thresholds = {
            "GDPR": 65,
            "FCRA": 60,
            "CCPA": 70,
            "GLBA": 75,
            "EU_AI_ACT": 80,
            "FINRA": 70
        }
        return thresholds.get(regulatory_framework, 65)
