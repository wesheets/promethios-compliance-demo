"""
FINRA Framework for the Dynamic Regulatory Mapping System.

This module implements the FINRA regulatory framework, mapping trust factors
to specific requirements from the Financial Industry Regulatory Authority.
"""

from .base_framework import RegulatoryFramework

class FINRAFramework(RegulatoryFramework):
    """FINRA regulatory framework implementation."""
    
    def __init__(self):
        """Initialize the FINRA framework with its requirements and mappings."""
        super().__init__(
            name="FINRA",
            description="Financial Industry Regulatory Authority framework, focusing on investor protection and market integrity"
        )
        
        # Add key requirements from FINRA regulations
        self.add_requirement(
            "FINRA-01",
            "Suitability: Recommendations must be suitable for the specific customer",
            "Suitability"
        )
        
        self.add_requirement(
            "FINRA-02",
            "Disclosure: Clear disclosure of risks, costs, and conflicts of interest",
            "Disclosure"
        )
        
        self.add_requirement(
            "FINRA-03",
            "Fair Pricing: Reasonable and fair pricing of financial products",
            "Pricing"
        )
        
        self.add_requirement(
            "FINRA-04",
            "Risk Assessment: Proper assessment of customer risk tolerance",
            "Risk"
        )
        
        self.add_requirement(
            "FINRA-05",
            "Record Keeping: Maintenance of accurate and complete records",
            "Documentation"
        )
        
        self.add_requirement(
            "FINRA-06",
            "Supervision: Adequate supervision of automated systems",
            "Governance"
        )
        
        self.add_requirement(
            "FINRA-07",
            "Data Security: Protection of customer data and financial information",
            "Security"
        )
        
        # Map trust factors to requirements
        self.map_factor_to_requirements(
            "data_quality",
            ["FINRA-05", "FINRA-04", "FINRA-07"],
            weight=1.1
        )
        
        self.map_factor_to_requirements(
            "model_confidence",
            ["FINRA-04", "FINRA-01", "FINRA-06"],
            weight=1.2
        )
        
        self.map_factor_to_requirements(
            "regulatory_alignment",
            ["FINRA-05", "FINRA-02", "FINRA-06"],
            weight=1.4
        )
        
        self.map_factor_to_requirements(
            "ethical_considerations",
            ["FINRA-01", "FINRA-02", "FINRA-03"],
            weight=1.0
        )
    
    def evaluate_compliance(self, trust_evaluation_results):
        """
        Evaluate compliance with FINRA regulations based on trust evaluation results.
        
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
            
            # Determine compliance (FINRA has a moderate threshold)
            is_compliant = req_score >= 70
            
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
        
        # FINRA requires moderate compliance (at least 80% of requirements)
        overall_compliant = compliance_percentage >= 80
        
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
            "Suitability": "Improve customer suitability assessment by gathering more detailed financial information",
            "Disclosure": "Enhance disclosure documentation to more clearly explain risks and costs",
            "Pricing": "Review pricing model to ensure fair and reasonable rates for all customers",
            "Risk": "Strengthen risk assessment methodology with more comprehensive factors",
            "Documentation": "Improve record keeping practices with more detailed transaction logs",
            "Governance": "Enhance supervision of automated systems with additional review checkpoints",
            "Security": "Strengthen data security measures to better protect customer information"
        }
        
        category = critical_req["category"]
        suggestion = remediation_templates.get(category, "Review and address compliance issues")
        
        return {
            "priority_requirement": critical_req,
            "suggestion": suggestion,
            "additional_requirements": non_compliant_reqs[1:3] if len(non_compliant_reqs) > 1 else []
        }
