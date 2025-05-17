"""
Unit tests for the OpenAI Explainer module.

This module contains tests for the OpenAI-powered conversational explainability feature.
"""

import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from compliance_api.openai_explainer import OpenAIExplainer

class TestOpenAIExplainer(unittest.TestCase):
    """Tests for the OpenAIExplainer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the OpenAI API key
        os.environ["OPENAI_API_KEY"] = "test_api_key"
        
        # Create the explainer
        self.explainer = OpenAIExplainer()
        
        # Sample decision data for testing
        self.decision_data = {
            "decision_id": "decision_123",
            "application_id": "app_456",
            "is_compliant": False,
            "compliance_score": 65.0,
            "framework": "EU_AI_ACT",
            "timestamp": "2025-05-17T10:30:00Z",
            "primary_reason": "Insufficient data quality and transparency",
            "trust_factors": {
                "overall_score": 70.0,
                "factors": {
                    "data_quality": {
                        "score": 60.0,
                        "details": ["Missing employment verification", "Inconsistent income data"],
                        "description": "The application has data quality issues"
                    },
                    "model_confidence": {
                        "score": 75.0,
                        "details": ["Model uncertainty is moderate"],
                        "description": "The model's confidence in its prediction is moderate"
                    },
                    "regulatory_alignment": {
                        "score": 65.0,
                        "details": ["Missing transparency documentation"],
                        "description": "The application does not fully align with regulatory requirements"
                    },
                    "ethical_considerations": {
                        "score": 80.0,
                        "details": ["No significant ethical concerns"],
                        "description": "The application does not raise significant ethical concerns"
                    }
                }
            },
            "requirements": [
                {
                    "id": "eu_ai_act_transparency",
                    "name": "Transparency",
                    "status": "Non-Compliant",
                    "details": "Missing documentation on model training and data sources"
                },
                {
                    "id": "eu_ai_act_data_quality",
                    "name": "Data Quality",
                    "status": "Non-Compliant",
                    "details": "Inconsistent income data and missing employment verification"
                },
                {
                    "id": "eu_ai_act_human_oversight",
                    "name": "Human Oversight",
                    "status": "Compliant",
                    "details": "Adequate human oversight mechanisms in place"
                }
            ]
        }
    
    @patch('requests.post')
    def test_explain_decision(self, mock_post):
        """Test generating an explanation for a decision."""
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This loan application was found non-compliant with the EU AI Act primarily due to data quality issues and lack of transparency. The compliance score was 65%, below the required threshold of 80%. Specifically, there were inconsistencies in the income data and missing employment verification, which affected the data quality score (60%). Additionally, the application lacked proper documentation on model training and data sources, violating the transparency requirements of the EU AI Act."
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Test the explain_decision method
        explanation = self.explainer.explain_decision(self.decision_data)
        
        # Check that the explanation is a non-empty string
        self.assertIsInstance(explanation, str)
        self.assertTrue(len(explanation) > 0)
        
        # Check that the API was called with the correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        self.assertEqual(call_args["headers"]["Authorization"], "Bearer test_api_key")
        self.assertEqual(call_args["json"]["model"], "gpt-4")
        self.assertGreaterEqual(len(call_args["json"]["messages"]), 2)
    
    @patch('requests.post')
    def test_explain_decision_with_query(self, mock_post):
        """Test generating an explanation for a decision with a specific query."""
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "The main data quality issues in this application are missing employment verification and inconsistent income data. These issues make it difficult to accurately assess the applicant's financial situation and repayment ability, which is crucial for compliance with the EU AI Act's requirements for high-risk AI systems in financial services."
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Test the explain_decision method with a query
        query = "What are the specific data quality issues and why do they matter?"
        explanation = self.explainer.explain_decision(self.decision_data, query)
        
        # Check that the explanation is a non-empty string
        self.assertIsInstance(explanation, str)
        self.assertTrue(len(explanation) > 0)
        
        # Check that the API was called with the correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        self.assertEqual(call_args["headers"]["Authorization"], "Bearer test_api_key")
        self.assertEqual(call_args["json"]["model"], "gpt-4")
        self.assertGreaterEqual(len(call_args["json"]["messages"]), 2)
        
        # Check that the query was included in the user message
        user_message = call_args["json"]["messages"][1]["content"]
        self.assertIn(query, user_message)
    
    @patch('requests.post')
    def test_generate_recommendations(self, mock_post):
        """Test generating recommendations based on application data and trust factors."""
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps([
                            {
                                "title": "Improve Data Quality",
                                "description": "Verify employment information and resolve inconsistencies in income data to improve the data quality score.",
                                "priority": "high"
                            },
                            {
                                "title": "Enhance Transparency Documentation",
                                "description": "Provide comprehensive documentation on model training procedures and data sources to meet EU AI Act transparency requirements.",
                                "priority": "high"
                            },
                            {
                                "title": "Increase Model Confidence",
                                "description": "Consider retraining the model with additional validated data to improve prediction confidence.",
                                "priority": "medium"
                            }
                        ])
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Extract application data and trust factors from the decision data
        application_data = {
            "application_id": self.decision_data["application_id"]
        }
        trust_factors = self.decision_data["trust_factors"]
        
        # Test the generate_recommendations method
        recommendations = self.explainer.generate_recommendations(application_data, trust_factors)
        
        # Check that recommendations is a non-empty list
        self.assertIsInstance(recommendations, list)
        self.assertTrue(len(recommendations) > 0)
        
        # Check that each recommendation has the expected fields
        for rec in recommendations:
            self.assertIn("title", rec)
            self.assertIn("description", rec)
            self.assertIn("priority", rec)
        
        # Check that the API was called with the correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        self.assertEqual(call_args["headers"]["Authorization"], "Bearer test_api_key")
        self.assertEqual(call_args["json"]["model"], "gpt-4")
        self.assertEqual(call_args["json"]["response_format"]["type"], "json_object")
    
    @patch('requests.post')
    def test_api_error_handling(self, mock_post):
        """Test handling of API errors."""
        # Mock an API error
        mock_post.side_effect = Exception("API error")
        
        # Test the explain_decision method with the error
        explanation = self.explainer.explain_decision(self.decision_data)
        
        # Check that an error message is returned
        self.assertIsInstance(explanation, str)
        self.assertIn("Error", explanation)
    
    def test_missing_api_key(self):
        """Test handling of missing API key."""
        # Remove the API key from environment
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        # Check that creating an explainer without an API key raises an error
        with self.assertRaises(ValueError):
            OpenAIExplainer()

if __name__ == "__main__":
    unittest.main()
