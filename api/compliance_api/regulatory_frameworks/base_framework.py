"""
Base Regulatory Framework for the Dynamic Regulatory Mapping System.

This module defines the abstract base class for all regulatory frameworks used in
mapping trust factors to specific regulatory requirements.
"""

class RegulatoryFramework:
    """Base class for all regulatory frameworks."""
    
    def __init__(self, name, description=None):
        """
        Initialize a regulatory framework.
        
        Args:
            name: Name of the regulatory framework
            description: Description of the framework (optional)
        """
        self.name = name
        self.description = description or ""
        self.requirements = []
        self.trust_factor_mappings = {}
        
    def add_requirement(self, requirement_id, description, category=None):
        """
        Add a regulatory requirement to the framework.
        
        Args:
            requirement_id: Unique identifier for the requirement
            description: Description of the requirement
            category: Category of the requirement (optional)
            
        Returns:
            dict: The added requirement
        """
        requirement = {
            "id": requirement_id,
            "description": description,
            "category": category
        }
        self.requirements.append(requirement)
        return requirement
    
    def map_factor_to_requirements(self, factor_id, requirement_ids, weight=1.0):
        """
        Map a trust factor to specific regulatory requirements.
        
        Args:
            factor_id: ID of the trust factor
            requirement_ids: List of requirement IDs to map to
            weight: Weight of this factor for these requirements (default: 1.0)
            
        Returns:
            dict: The mapping created
        """
        if factor_id not in self.trust_factor_mappings:
            self.trust_factor_mappings[factor_id] = []
            
        mapping = {
            "factor_id": factor_id,
            "requirement_ids": requirement_ids,
            "weight": weight
        }
        self.trust_factor_mappings[factor_id].append(mapping)
        return mapping
    
    def get_requirements_for_factor(self, factor_id):
        """
        Get all requirements mapped to a specific trust factor.
        
        Args:
            factor_id: ID of the trust factor
            
        Returns:
            list: List of requirement dictionaries
        """
        if factor_id not in self.trust_factor_mappings:
            return []
            
        # Get all requirement IDs for this factor
        requirement_ids = set()
        for mapping in self.trust_factor_mappings[factor_id]:
            requirement_ids.update(mapping["requirement_ids"])
            
        # Get the full requirement objects
        return [req for req in self.requirements if req["id"] in requirement_ids]
    
    def get_factors_for_requirement(self, requirement_id):
        """
        Get all trust factors mapped to a specific requirement.
        
        Args:
            requirement_id: ID of the requirement
            
        Returns:
            list: List of factor IDs with their weights
        """
        factors = []
        
        for factor_id, mappings in self.trust_factor_mappings.items():
            for mapping in mappings:
                if requirement_id in mapping["requirement_ids"]:
                    factors.append({
                        "factor_id": factor_id,
                        "weight": mapping["weight"]
                    })
                    break
                    
        return factors
    
    def evaluate_compliance(self, trust_evaluation_results):
        """
        Evaluate compliance with this regulatory framework based on trust evaluation results.
        Must be implemented by subclasses.
        
        Args:
            trust_evaluation_results: Results from the trust evaluation framework
            
        Returns:
            dict: Compliance evaluation results
        """
        raise NotImplementedError("Subclasses must implement evaluate_compliance()")
