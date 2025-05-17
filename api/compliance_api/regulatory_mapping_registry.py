"""
Regulatory Mapping Registry for the Dynamic Regulatory Mapping System.

This module implements the registry that manages regulatory frameworks
and provides mapping between trust factors and regulatory requirements.
"""

from .regulatory_frameworks import EUAIActFramework, FINRAFramework

class RegulatoryMappingRegistry:
    """Registry for managing regulatory frameworks and their mappings."""
    
    def __init__(self):
        """Initialize the registry with default frameworks."""
        self.frameworks = {}
        
        # Register default frameworks
        self.register_framework(EUAIActFramework())
        self.register_framework(FINRAFramework())
        
    def register_framework(self, framework):
        """
        Register a regulatory framework.
        
        Args:
            framework: RegulatoryFramework instance
            
        Returns:
            bool: True if registration was successful
        """
        if framework.name in self.frameworks:
            return False
            
        self.frameworks[framework.name] = framework
        return True
    
    def get_framework(self, framework_name):
        """
        Get a regulatory framework by name.
        
        Args:
            framework_name: Name of the framework
            
        Returns:
            RegulatoryFramework: The requested framework or None if not found
        """
        return self.frameworks.get(framework_name)
    
    def get_available_frameworks(self):
        """
        Get a list of available regulatory frameworks.
        
        Returns:
            list: List of framework names
        """
        return list(self.frameworks.keys())
    
    def evaluate_compliance(self, trust_evaluation_results, framework_name=None):
        """
        Evaluate compliance with a specific regulatory framework.
        
        Args:
            trust_evaluation_results: Results from the trust evaluation framework
            framework_name: Name of the framework to evaluate against (optional)
            
        Returns:
            dict: Compliance evaluation results
            
        Raises:
            ValueError: If framework_name is not found
        """
        # If no framework specified, use the one from the trust evaluation results
        if framework_name is None:
            framework_name = trust_evaluation_results.get("regulatory_framework", "EU_AI_ACT")
            
        # Get the framework
        framework = self.get_framework(framework_name)
        if not framework:
            raise ValueError(f"Unknown regulatory framework: {framework_name}")
            
        # Evaluate compliance
        return framework.evaluate_compliance(trust_evaluation_results)
    
    def get_requirements_for_factor(self, factor_id, framework_name=None):
        """
        Get all requirements mapped to a specific trust factor.
        
        Args:
            factor_id: ID of the trust factor
            framework_name: Name of the framework (optional, if None, get from all frameworks)
            
        Returns:
            dict: Dictionary mapping framework names to lists of requirements
        """
        if framework_name:
            framework = self.get_framework(framework_name)
            if not framework:
                return {}
                
            return {framework_name: framework.get_requirements_for_factor(factor_id)}
            
        # Get from all frameworks
        result = {}
        for name, framework in self.frameworks.items():
            requirements = framework.get_requirements_for_factor(factor_id)
            if requirements:
                result[name] = requirements
                
        return result
    
    def get_factors_for_requirement(self, requirement_id, framework_name):
        """
        Get all trust factors mapped to a specific requirement.
        
        Args:
            requirement_id: ID of the requirement
            framework_name: Name of the framework
            
        Returns:
            list: List of factor IDs with their weights
            
        Raises:
            ValueError: If framework_name is not found
        """
        framework = self.get_framework(framework_name)
        if not framework:
            raise ValueError(f"Unknown regulatory framework: {framework_name}")
            
        return framework.get_factors_for_requirement(requirement_id)
