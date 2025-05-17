"""
Unit tests for the Regulatory Frameworks module.

This module contains tests for the regulatory framework classes and the regulatory mapping registry.
"""

import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from compliance_api.regulatory_frameworks.base_framework import RegulatoryFramework
from compliance_api.regulatory_frameworks.eu_ai_act_framework import EUAIActFramework
from compliance_api.regulatory_frameworks.finra_framework import FINRAFramework
from compliance_api.regulatory_mapping_registry import RegulatoryMappingRegistry

class TestBaseRegulatoryFramework(unittest.TestCase):
    """Tests for the RegulatoryFramework base class."""
    
    def test_abstract_methods(self):
        """Test that RegulatoryFramework is abstract and cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            RegulatoryFramework()
    
    def test_subclass_implementation(self):
        """Test that a proper subclass can be instantiated."""
        class TestFramework(RegulatoryFramework):
            def get_requirements(self):
                return [{"id": "req1", "name": "Test Requirement", "description": "A test requirement"}]
            
            def evaluate_compliance(self, application_data, trust_factors):
                return True, 95.0, "Compliant", []
        
        framework = TestFramework()
        self.assertIsInstance(framework, RegulatoryFramework)

class TestEUAIActFramework(unittest.TestCase):
    """Tests for the EUAIActFramework class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.framework = EUAIActFramework()
        
        # Sample application and trust factors for testing
        self.application = {
            "application_id": "TEST_001",
            "amount": 10000,
            "purpose": "debt_consolidation",
            "grade": "A",
            "interest_rate": 5.0,
            "term": 36,
            "employment_length": 5,
            "home_ownership": "MORTGAGE",
            "annual_income": 75000,
            "verification_status": "Verified",
            "dti": 15.0
        }
        
        self.trust_factors = {
            "overall_score": 88.0,
            "is_trustworthy": True,
            "factors": {
                "data_quality": {
                    "score": 90.0,
                    "details": ["Good data quality"],
                    "description": "Data is complete and consistent"
                },
                "model_confidence": {
                    "score": 85.0,
                    "details": ["Good model confidence"],
                    "description": "Model predictions are reliable"
                },
                "regulatory_alignment": {
                    "score": 95.0,
                    "details": ["Excellent regulatory alignment"],
                    "description": "Fully compliant with regulations"
                },
                "ethical_considerations": {
                    "score": 80.0,
                    "details": ["Good ethical considerations"],
                    "description": "No significant ethical concerns"
                }
            }
        }
    
    def test_get_requirements(self):
        """Test that the framework returns the expected requirements."""
        requirements = self.framework.get_requirements()
        
        # Check that requirements is a non-empty list
        self.assertIsInstance(requirements, list)
        self.assertTrue(len(requirements) > 0)
        
        # Check that each requirement has the expected fields
        for req in requirements:
            self.assertIn("id", req)
            self.assertIn("name", req)
            self.assertIn("description", req)
    
    def test_evaluate_compliance_compliant(self):
        """Test evaluation of a compliant application."""
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            self.application, self.trust_factors
        )
        
        # Check that the application is considered compliant
        self.assertTrue(is_compliant)
        self.assertGreaterEqual(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)
    
    def test_evaluate_compliance_non_compliant_data_quality(self):
        """Test evaluation of an application with poor data quality."""
        # Modify trust factors to have low data quality score
        trust_factors = self.trust_factors.copy()
        trust_factors["factors"]["data_quality"]["score"] = 50.0
        trust_factors["overall_score"] = 75.0
        
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            self.application, trust_factors
        )
        
        # Check that the application is considered non-compliant
        self.assertFalse(is_compliant)
        self.assertLess(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)
    
    def test_evaluate_compliance_non_compliant_ethical(self):
        """Test evaluation of an application with ethical concerns."""
        # Modify trust factors to have low ethical considerations score
        trust_factors = self.trust_factors.copy()
        trust_factors["factors"]["ethical_considerations"]["score"] = 40.0
        trust_factors["overall_score"] = 75.0
        
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            self.application, trust_factors
        )
        
        # Check that the application is considered non-compliant
        self.assertFalse(is_compliant)
        self.assertLess(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)

class TestFINRAFramework(unittest.TestCase):
    """Tests for the FINRAFramework class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.framework = FINRAFramework()
        
        # Sample application and trust factors for testing
        self.application = {
            "application_id": "TEST_001",
            "amount": 10000,
            "purpose": "debt_consolidation",
            "grade": "A",
            "interest_rate": 5.0,
            "term": 36,
            "employment_length": 5,
            "home_ownership": "MORTGAGE",
            "annual_income": 75000,
            "verification_status": "Verified",
            "dti": 15.0,
            "delinq_2yrs": 0,
            "mths_since_last_delinq": None
        }
        
        self.trust_factors = {
            "overall_score": 88.0,
            "is_trustworthy": True,
            "factors": {
                "data_quality": {
                    "score": 90.0,
                    "details": ["Good data quality"],
                    "description": "Data is complete and consistent"
                },
                "model_confidence": {
                    "score": 85.0,
                    "details": ["Good model confidence"],
                    "description": "Model predictions are reliable"
                },
                "regulatory_alignment": {
                    "score": 95.0,
                    "details": ["Excellent regulatory alignment"],
                    "description": "Fully compliant with regulations"
                },
                "ethical_considerations": {
                    "score": 80.0,
                    "details": ["Good ethical considerations"],
                    "description": "No significant ethical concerns"
                }
            }
        }
    
    def test_get_requirements(self):
        """Test that the framework returns the expected requirements."""
        requirements = self.framework.get_requirements()
        
        # Check that requirements is a non-empty list
        self.assertIsInstance(requirements, list)
        self.assertTrue(len(requirements) > 0)
        
        # Check that each requirement has the expected fields
        for req in requirements:
            self.assertIn("id", req)
            self.assertIn("name", req)
            self.assertIn("description", req)
    
    def test_evaluate_compliance_compliant(self):
        """Test evaluation of a compliant application."""
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            self.application, self.trust_factors
        )
        
        # Check that the application is considered compliant
        self.assertTrue(is_compliant)
        self.assertGreaterEqual(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)
    
    def test_evaluate_compliance_non_compliant_delinquency(self):
        """Test evaluation of an application with recent delinquencies."""
        # Modify application to have recent delinquencies
        application = self.application.copy()
        application["delinq_2yrs"] = 2
        application["mths_since_last_delinq"] = 3
        
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            application, self.trust_factors
        )
        
        # Check that the application is considered non-compliant
        self.assertFalse(is_compliant)
        self.assertLess(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)
    
    def test_evaluate_compliance_non_compliant_high_dti(self):
        """Test evaluation of an application with high debt-to-income ratio."""
        # Modify application to have high DTI
        application = self.application.copy()
        application["dti"] = 45.0
        
        is_compliant, score, reason, details = self.framework.evaluate_compliance(
            application, self.trust_factors
        )
        
        # Check that the application is considered non-compliant
        self.assertFalse(is_compliant)
        self.assertLess(score, 80.0)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(details, list)

class TestRegulatoryMappingRegistry(unittest.TestCase):
    """Tests for the RegulatoryMappingRegistry class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock frameworks
        self.eu_ai_act = MagicMock()
        self.eu_ai_act.get_requirements.return_value = [
            {"id": "eu1", "name": "Transparency", "description": "Ensure transparency in AI systems"},
            {"id": "eu2", "name": "Human Oversight", "description": "Ensure human oversight of AI systems"}
        ]
        self.eu_ai_act.evaluate_compliance.return_value = (True, 90.0, "Compliant", [])
        
        self.finra = MagicMock()
        self.finra.get_requirements.return_value = [
            {"id": "finra1", "name": "Fair Lending", "description": "Ensure fair lending practices"},
            {"id": "finra2", "name": "Risk Assessment", "description": "Proper risk assessment procedures"}
        ]
        self.finra.evaluate_compliance.return_value = (True, 85.0, "Compliant", [])
        
        # Create the registry with mock frameworks
        self.registry = RegulatoryMappingRegistry()
        self.registry.register_framework("EU_AI_ACT", self.eu_ai_act)
        self.registry.register_framework("FINRA", self.finra)
        
        # Sample application and trust factors
        self.application = {"application_id": "TEST_001"}
        self.trust_factors = {
            "overall_score": 88.0,
            "is_trustworthy": True,
            "factors": {
                "data_quality": {"score": 90.0},
                "model_confidence": {"score": 85.0},
                "regulatory_alignment": {"score": 95.0},
                "ethical_considerations": {"score": 80.0}
            }
        }
    
    def test_get_frameworks(self):
        """Test getting the list of registered frameworks."""
        frameworks = self.registry.get_frameworks()
        
        # Check that both frameworks are registered
        self.assertEqual(len(frameworks), 2)
        self.assertIn("EU_AI_ACT", frameworks)
        self.assertIn("FINRA", frameworks)
    
    def test_get_requirements(self):
        """Test getting requirements for a specific framework."""
        eu_requirements = self.registry.get_requirements("EU_AI_ACT")
        finra_requirements = self.registry.get_requirements("FINRA")
        
        # Check that the correct requirements are returned
        self.assertEqual(len(eu_requirements), 2)
        self.assertEqual(eu_requirements[0]["id"], "eu1")
        
        self.assertEqual(len(finra_requirements), 2)
        self.assertEqual(finra_requirements[0]["id"], "finra1")
    
    def test_evaluate_compliance(self):
        """Test evaluating compliance against a specific framework."""
        result = self.registry.evaluate_compliance(
            "EU_AI_ACT", self.application, self.trust_factors
        )
        
        # Check that the result contains the expected fields
        self.assertIn("is_compliant", result)
        self.assertIn("compliance_score", result)
        self.assertIn("reason", result)
        self.assertIn("details", result)
        self.assertIn("framework", result)
        self.assertIn("requirements", result)
        
        # Check that the compliance evaluation is correct
        self.assertTrue(result["is_compliant"])
        self.assertEqual(result["compliance_score"], 90.0)
        self.assertEqual(result["framework"], "EU_AI_ACT")
    
    def test_evaluate_compliance_unknown_framework(self):
        """Test evaluating compliance against an unknown framework."""
        with self.assertRaises(ValueError):
            self.registry.evaluate_compliance(
                "UNKNOWN", self.application, self.trust_factors
            )
    
    def test_evaluate_all_frameworks(self):
        """Test evaluating compliance against all frameworks."""
        results = self.registry.evaluate_all_frameworks(
            self.application, self.trust_factors
        )
        
        # Check that results for both frameworks are returned
        self.assertEqual(len(results), 2)
        self.assertIn("EU_AI_ACT", results)
        self.assertIn("FINRA", results)
        
        # Check that each result contains the expected fields
        for framework, result in results.items():
            self.assertIn("is_compliant", result)
            self.assertIn("compliance_score", result)
            self.assertIn("reason", result)
            self.assertIn("details", result)
            self.assertIn("framework", result)
            self.assertIn("requirements", result)

if __name__ == "__main__":
    unittest.main()
