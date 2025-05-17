"""
Unit tests for the Trust Factors module.

This module contains tests for the trust factor classes and the trust evaluation framework.
"""

import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from compliance_api.trust_factors.base_factor import BaseTrustFactor
from compliance_api.trust_factors.data_quality_factor import DataQualityFactor
from compliance_api.trust_factors.model_confidence_factor import ModelConfidenceFactor
from compliance_api.trust_factors.regulatory_alignment_factor import RegulatoryAlignmentFactor
from compliance_api.trust_factors.ethical_considerations_factor import EthicalConsiderationsFactor
from compliance_api.trust_evaluation_framework import TrustEvaluationFramework

class TestBaseTrustFactor(unittest.TestCase):
    """Tests for the BaseTrustFactor class."""
    
    def test_abstract_methods(self):
        """Test that BaseTrustFactor is abstract and cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            BaseTrustFactor()
    
    def test_subclass_implementation(self):
        """Test that a proper subclass can be instantiated."""
        class TestFactor(BaseTrustFactor):
            def evaluate(self, application_data):
                return 85.0, ["Test detail"], "Test description"
        
        factor = TestFactor()
        self.assertIsInstance(factor, BaseTrustFactor)

class TestDataQualityFactor(unittest.TestCase):
    """Tests for the DataQualityFactor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factor = DataQualityFactor()
        
        # Sample application data for testing
        self.complete_application = {
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
            "earliest_credit_line": "2010-01-01",
            "inq_last_6mths": 1,
            "mths_since_last_delinq": None,
            "open_acc": 5,
            "pub_rec": 0,
            "revol_bal": 10000,
            "revol_util": 30.0,
            "total_acc": 10
        }
        
        self.incomplete_application = {
            "application_id": "TEST_002",
            "amount": 15000,
            "purpose": "home_improvement",
            # Missing several fields
            "grade": "B",
            "interest_rate": 7.5,
            "term": 60
        }
        
        self.inconsistent_application = {
            "application_id": "TEST_003",
            "amount": 20000,
            "purpose": "debt_consolidation",
            "grade": "C",
            "interest_rate": 10.0,
            "term": 36,
            "employment_length": 2,
            "home_ownership": "RENT",
            "annual_income": 50000,
            "verification_status": "Not Verified",
            "dti": 40.0,  # Inconsistent with income and amount
            "delinq_2yrs": 2,
            "earliest_credit_line": "2020-01-01",
            "inq_last_6mths": 5,  # High number of inquiries
            "mths_since_last_delinq": 3,
            "open_acc": 10,
            "pub_rec": 1,
            "revol_bal": 30000,  # Inconsistent with income
            "revol_util": 90.0,  # Very high utilization
            "total_acc": 12
        }
    
    def test_evaluate_complete_application(self):
        """Test evaluation of a complete application."""
        score, details, description = self.factor.evaluate(self.complete_application)
        
        # Check that the score is high for a complete application
        self.assertGreaterEqual(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_incomplete_application(self):
        """Test evaluation of an incomplete application."""
        score, details, description = self.factor.evaluate(self.incomplete_application)
        
        # Check that the score is lower for an incomplete application
        self.assertLess(score, 70.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_inconsistent_application(self):
        """Test evaluation of an application with inconsistent data."""
        score, details, description = self.factor.evaluate(self.inconsistent_application)
        
        # Check that the score is lower for an inconsistent application
        self.assertLess(score, 80.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)

class TestModelConfidenceFactor(unittest.TestCase):
    """Tests for the ModelConfidenceFactor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factor = ModelConfidenceFactor()
        
        # Sample application data for testing
        self.high_confidence_application = {
            "application_id": "TEST_001",
            "model_confidence": 0.95,
            "prediction_probability": 0.92,
            "model_version": "v2.0",
            "feature_importance": {
                "income": 0.3,
                "credit_score": 0.25,
                "loan_amount": 0.2,
                "employment_length": 0.15,
                "debt_to_income": 0.1
            }
        }
        
        self.medium_confidence_application = {
            "application_id": "TEST_002",
            "model_confidence": 0.75,
            "prediction_probability": 0.68,
            "model_version": "v1.5",
            "feature_importance": {
                "income": 0.2,
                "credit_score": 0.2,
                "loan_amount": 0.2,
                "employment_length": 0.2,
                "debt_to_income": 0.2
            }
        }
        
        self.low_confidence_application = {
            "application_id": "TEST_003",
            "model_confidence": 0.55,
            "prediction_probability": 0.51,
            "model_version": "v1.0",
            "feature_importance": {
                "income": 0.5,
                "credit_score": 0.1,
                "loan_amount": 0.1,
                "employment_length": 0.1,
                "debt_to_income": 0.2
            }
        }
    
    def test_evaluate_high_confidence(self):
        """Test evaluation of an application with high model confidence."""
        score, details, description = self.factor.evaluate(self.high_confidence_application)
        
        # Check that the score is high for high confidence
        self.assertGreaterEqual(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_medium_confidence(self):
        """Test evaluation of an application with medium model confidence."""
        score, details, description = self.factor.evaluate(self.medium_confidence_application)
        
        # Check that the score is medium for medium confidence
        self.assertGreaterEqual(score, 70.0)
        self.assertLess(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_low_confidence(self):
        """Test evaluation of an application with low model confidence."""
        score, details, description = self.factor.evaluate(self.low_confidence_application)
        
        # Check that the score is low for low confidence
        self.assertLess(score, 70.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_missing_confidence(self):
        """Test evaluation of an application with missing confidence data."""
        application = {"application_id": "TEST_004"}
        score, details, description = self.factor.evaluate(application)
        
        # Check that the score is very low for missing confidence data
        self.assertLess(score, 50.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)

class TestRegulatoryAlignmentFactor(unittest.TestCase):
    """Tests for the RegulatoryAlignmentFactor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factor = RegulatoryAlignmentFactor()
        
        # Sample application data for testing
        self.compliant_application = {
            "application_id": "TEST_001",
            "transparency_score": 95,
            "fairness_score": 90,
            "accountability_measures": ["audit_trail", "human_oversight", "appeals_process"],
            "documentation_level": "comprehensive",
            "regulatory_checks": {
                "eu_ai_act": True,
                "finra": True,
                "internal_policy": True
            }
        }
        
        self.partially_compliant_application = {
            "application_id": "TEST_002",
            "transparency_score": 75,
            "fairness_score": 80,
            "accountability_measures": ["audit_trail"],
            "documentation_level": "partial",
            "regulatory_checks": {
                "eu_ai_act": True,
                "finra": False,
                "internal_policy": True
            }
        }
        
        self.non_compliant_application = {
            "application_id": "TEST_003",
            "transparency_score": 50,
            "fairness_score": 60,
            "accountability_measures": [],
            "documentation_level": "minimal",
            "regulatory_checks": {
                "eu_ai_act": False,
                "finra": False,
                "internal_policy": True
            }
        }
    
    def test_evaluate_compliant_application(self):
        """Test evaluation of a fully compliant application."""
        score, details, description = self.factor.evaluate(self.compliant_application)
        
        # Check that the score is high for a compliant application
        self.assertGreaterEqual(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_partially_compliant_application(self):
        """Test evaluation of a partially compliant application."""
        score, details, description = self.factor.evaluate(self.partially_compliant_application)
        
        # Check that the score is medium for a partially compliant application
        self.assertGreaterEqual(score, 70.0)
        self.assertLess(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_non_compliant_application(self):
        """Test evaluation of a non-compliant application."""
        score, details, description = self.factor.evaluate(self.non_compliant_application)
        
        # Check that the score is low for a non-compliant application
        self.assertLess(score, 70.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_missing_compliance_data(self):
        """Test evaluation of an application with missing compliance data."""
        application = {"application_id": "TEST_004"}
        score, details, description = self.factor.evaluate(application)
        
        # Check that the score is very low for missing compliance data
        self.assertLess(score, 50.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)

class TestEthicalConsiderationsFactor(unittest.TestCase):
    """Tests for the EthicalConsiderationsFactor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factor = EthicalConsiderationsFactor()
        
        # Sample application data for testing
        self.ethical_application = {
            "application_id": "TEST_001",
            "bias_score": 5.0,  # Low bias (good)
            "fairness_metrics": {
                "demographic_parity": 0.95,
                "equal_opportunity": 0.92,
                "disparate_impact": 0.98
            },
            "protected_attributes_analysis": {
                "gender": "balanced",
                "race": "balanced",
                "age": "balanced"
            },
            "ethical_review_status": "approved"
        }
        
        self.questionable_application = {
            "application_id": "TEST_002",
            "bias_score": 15.0,  # Medium bias
            "fairness_metrics": {
                "demographic_parity": 0.75,
                "equal_opportunity": 0.78,
                "disparate_impact": 0.82
            },
            "protected_attributes_analysis": {
                "gender": "slight_imbalance",
                "race": "moderate_imbalance",
                "age": "balanced"
            },
            "ethical_review_status": "pending"
        }
        
        self.unethical_application = {
            "application_id": "TEST_003",
            "bias_score": 30.0,  # High bias (bad)
            "fairness_metrics": {
                "demographic_parity": 0.55,
                "equal_opportunity": 0.60,
                "disparate_impact": 0.65
            },
            "protected_attributes_analysis": {
                "gender": "significant_imbalance",
                "race": "significant_imbalance",
                "age": "moderate_imbalance"
            },
            "ethical_review_status": "rejected"
        }
    
    def test_evaluate_ethical_application(self):
        """Test evaluation of an ethically sound application."""
        score, details, description = self.factor.evaluate(self.ethical_application)
        
        # Check that the score is high for an ethical application
        self.assertGreaterEqual(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_questionable_application(self):
        """Test evaluation of an application with questionable ethics."""
        score, details, description = self.factor.evaluate(self.questionable_application)
        
        # Check that the score is medium for a questionable application
        self.assertGreaterEqual(score, 70.0)
        self.assertLess(score, 90.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_unethical_application(self):
        """Test evaluation of an unethical application."""
        score, details, description = self.factor.evaluate(self.unethical_application)
        
        # Check that the score is low for an unethical application
        self.assertLess(score, 70.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)
    
    def test_evaluate_missing_ethics_data(self):
        """Test evaluation of an application with missing ethics data."""
        application = {"application_id": "TEST_004"}
        score, details, description = self.factor.evaluate(application)
        
        # Check that the score is very low for missing ethics data
        self.assertLess(score, 50.0)
        self.assertIsInstance(details, list)
        self.assertIsInstance(description, str)

class TestTrustEvaluationFramework(unittest.TestCase):
    """Tests for the TrustEvaluationFramework class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock factors
        self.data_quality_factor = MagicMock()
        self.data_quality_factor.evaluate.return_value = (90.0, ["Good data quality"], "Data is complete and consistent")
        
        self.model_confidence_factor = MagicMock()
        self.model_confidence_factor.evaluate.return_value = (85.0, ["Good model confidence"], "Model predictions are reliable")
        
        self.regulatory_alignment_factor = MagicMock()
        self.regulatory_alignment_factor.evaluate.return_value = (95.0, ["Excellent regulatory alignment"], "Fully compliant with regulations")
        
        self.ethical_considerations_factor = MagicMock()
        self.ethical_considerations_factor.evaluate.return_value = (80.0, ["Good ethical considerations"], "No significant ethical concerns")
        
        # Create the framework with mock factors
        self.framework = TrustEvaluationFramework()
        self.framework.register_factor("data_quality", self.data_quality_factor, weight=0.25)
        self.framework.register_factor("model_confidence", self.model_confidence_factor, weight=0.25)
        self.framework.register_factor("regulatory_alignment", self.regulatory_alignment_factor, weight=0.25)
        self.framework.register_factor("ethical_considerations", self.ethical_considerations_factor, weight=0.25)
        
        # Sample application data
        self.application = {"application_id": "TEST_001"}
    
    def test_evaluate_application(self):
        """Test evaluation of an application using the framework."""
        result = self.framework.evaluate_application(self.application)
        
        # Check that the result contains the expected fields
        self.assertIn("overall_score", result)
        self.assertIn("factors", result)
        self.assertIn("is_trustworthy", result)
        self.assertIn("explanation", result)
        
        # Check that all factors are included in the result
        self.assertIn("data_quality", result["factors"])
        self.assertIn("model_confidence", result["factors"])
        self.assertIn("regulatory_alignment", result["factors"])
        self.assertIn("ethical_considerations", result["factors"])
        
        # Check that the overall score is calculated correctly
        expected_score = (90.0 * 0.25) + (85.0 * 0.25) + (95.0 * 0.25) + (80.0 * 0.25)
        self.assertAlmostEqual(result["overall_score"], expected_score)
        
        # Check that the trustworthiness is determined correctly
        self.assertTrue(result["is_trustworthy"])
    
    def test_evaluate_application_with_custom_threshold(self):
        """Test evaluation with a custom trustworthiness threshold."""
        # Set a very high threshold that the application won't meet
        self.framework.trustworthiness_threshold = 95.0
        
        result = self.framework.evaluate_application(self.application)
        
        # Check that the application is not considered trustworthy with the high threshold
        self.assertFalse(result["is_trustworthy"])
    
    def test_evaluate_application_with_custom_weights(self):
        """Test evaluation with custom factor weights."""
        # Create a new framework with custom weights
        framework = TrustEvaluationFramework()
        framework.register_factor("data_quality", self.data_quality_factor, weight=0.4)
        framework.register_factor("model_confidence", self.model_confidence_factor, weight=0.3)
        framework.register_factor("regulatory_alignment", self.regulatory_alignment_factor, weight=0.2)
        framework.register_factor("ethical_considerations", self.ethical_considerations_factor, weight=0.1)
        
        result = framework.evaluate_application(self.application)
        
        # Check that the overall score is calculated correctly with the custom weights
        expected_score = (90.0 * 0.4) + (85.0 * 0.3) + (95.0 * 0.2) + (80.0 * 0.1)
        self.assertAlmostEqual(result["overall_score"], expected_score)

if __name__ == "__main__":
    unittest.main()
