"""
EU AI Act Framework for the Dynamic Regulatory Mapping System.

This module implements the EU AI Act regulatory framework, mapping trust factors
to specific requirements from the European Union's Artificial Intelligence Act.
"""

from .base_framework import RegulatoryFramework

class EUAIActFramework(RegulatoryFramework):
    """EU AI Act regulatory framework implementation."""
    
    def __init__(self):
        """Initialize the EU AI Act framework with its requirements and mappings."""
        super().__init__(
            name="EU_AI_ACT",
            description="European Union Artificial Intelligence Act, focusing on transparency, fairness, and accountability in AI systems"
        )
        
        # Add key requirements from the EU AI Act
        self.add_requirement(
            "EUAI-01",
            "Transparency: AI systems must provide clear information about their capabilities and limitations",
            "Transparency"
        )
        
        self.add_requirement(
            "EUAI-02",
            "Fairness: AI systems must avoid unfair bias and discrimination",
            "Fairness"
        )
        
        self.add_requirement(
            "EUAI-03",
            "Human Oversight: AI systems must enable effective oversight by humans",
            "Governance"
        )
        
        self.add_requirement(
            "EUAI-04",
            "Robustness: AI systems must be technically robust and accurate",
            "Technical"
        )
        
        self.add_requirement(
            "EUAI-05",
            "Data Quality: AI systems must use high-quality training and operational data",
            "Data"
        )
        
        self.add_requirement(
            "EUAI-06",
            "Documentation: AI systems must maintain comprehensive documentation of development and operation",
            "Documentation"
        )
        
        self.add_requirement(
            "EUAI-07",
            "Risk Management: AI systems must implement appropriate risk management measures",
            "Risk"
        )
        
        # Map trust factors to requirements
        self.map_factor_to_requirements(
            "data_quality",
            ["EUAI-05", "EUAI-04", "EUAI-07"],
            weight=1.2
        )
        
        self.map_factor_to_requirements(
            "model_confidence",
            ["EUAI-04", "EUAI-01", "EUAI-07"],
            weight=1.0
        )
        
        self.map_factor_to_requirements(
            "regulatory_alignment",
            ["EUAI-06", "EUAI-03", "EUAI-01"],
            weight=1.5
        )
        
        self.map_factor_to_requirements(
            "ethical_considerations",
            ["EUAI-02", "EUAI-03", "EUAI-07"],
            weight=1.3
        )
    
    def evaluate_compliance(self, trust_evaluation_results):
        """
        Evaluate compliance with the EU AI Act based on trust evaluation results.
        
        Args:
            trust_evaluation_results: Results from the trust evaluation framework
            
        Returns:
            dict: Compliance evaluation results
        """
        # Extract factor scores from trust evaluation results
        factor_scores = {}
        for factor_id, factor_data in trust_evaluation_results["factors"].items():
            factor_scores[factor_id] = factor_data["score"]
        
        # Evaluate compliance for each requirement
        requirement_compliance = {}
        for req in self.requirements:
            req_id = req["id"]
            factors = self.get_factors_for_requirement(req_id)
            
            if not factors:
                # No factors mapped to this requirement
                requirement_compliance[req_id] = {
                    "compliant": False,
                    "score": 0,
                    "description": req["description"],
                    "category": req["category"],
                    "factors": []
                }
                continue
            
            # Calculate weighted score for this requirement
            weighted_sum = 0
            total_weight = 0
            req_factors = []
            
            for factor in factors:
                factor_id = factor["factor_id"]
                weight = factor["weight"]
                score = factor_scores.get(factor_id, 0)
                
                weighted_sum += score * weight
                total_weight += weight
                
                req_factors.append({
                    "factor_id": factor_id,
                    "score": score,
                    "weight": weight
                })
            
            req_score = weighted_sum / total_weight if total_weight > 0 else 0
            
            # Determine compliance (EU AI Act has a high threshold)
            is_compliant = req_score >= 75
            
            requirement_compliance[req_id] = {
                "compliant": is_compliant,
                "score": req_score,
                "description": req["description"],
                "category": req["category"],
                "factors": req_factors
            }
        
        # Calculate overall compliance
        compliant_reqs = sum(1 for req_data in requirement_compliance.values() if req_data["compliant"])
        total_reqs = len(requirement_compliance)
        compliance_percentage = (compliant_reqs / total_reqs) * 100 if total_reqs > 0 else 0
        
        # EU AI Act requires high compliance (at least 85% of requirements)
        overall_compliant = compliance_percentage >= 85
        
        # Identify non-compliant requirements for remediation
        non_compliant_reqs = [
            {
                "id": req_id,
                "description": req_data["description"],
                "score": req_data["score"],
                "category": req_data["category"]
            }
            for req_id, req_data in requirement_compliance.items()
            if not req_data["compliant"]
        ]
        
        # Sort by score (lowest first)
        non_compliant_reqs.sort(key=lambda x: x["score"])
        
        return {
            "framework": self.name,
            "description": self.description,
            "compliant": overall_compliant,
            "compliance_percentage": compliance_percentage,
            "compliant_requirements": compliant_reqs,
            "total_requirements": total_reqs,
            "requirement_compliance": requirement_compliance,
            "non_compliant_requirements": non_compliant_reqs,
            "remediation": self._generate_remediation(non_compliant_reqs) if non_compliant_reqs else None
        }
    
    def _generate_remediation(self, non_compliant_reqs):
        """Generate remediation suggestions for non-compliant requirements."""
        if not non_compliant_reqs:
            return None
        
        # Focus on the most critical non-compliant requirement
        critical_req = non_compliant_reqs[0]
        
        remediation_templates = {
            "Transparency": "Improve transparency by providing clearer explanations of decision factors and model limitations",
            "Fairness": "Address potential bias in the model by reviewing training data and decision criteria",
            "Governance": "Enhance human oversight capabilities by implementing additional review checkpoints",
            "Technical": "Improve model robustness through additional testing and validation",
            "Data": "Enhance data quality by implementing stricter validation and cleaning processes",
            "Documentation": "Improve documentation of model development, training, and decision processes",
            "Risk": "Strengthen risk management by implementing additional controls and monitoring"
        }
        
        category = critical_req["category"]
        suggestion = remediation_templates.get(category, "Review and address compliance issues")
        
        return {
            "priority_requirement": critical_req,
            "suggestion": suggestion,
            "additional_requirements": non_compliant_reqs[1:3] if len(non_compliant_reqs) > 1 else []
        }
