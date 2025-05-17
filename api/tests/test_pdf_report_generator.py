"""
Unit tests for the PDF Report Generator module.

This module contains tests for the PDF report generation functionality.
"""

import unittest
import sys
import os
import io
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from compliance_api.pdf_report_generator import ComplianceReportGenerator

class TestComplianceReportGenerator(unittest.TestCase):
    """Tests for the ComplianceReportGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = ComplianceReportGenerator()
        
        # Sample data for testing
        self.decision_data = {
            "decision_id": "decision_123",
            "application_id": "app_456",
            "is_compliant": False,
            "compliance_score": 65.0,
            "framework": "EU_AI_ACT",
            "timestamp": "2025-05-17T10:30:00Z",
            "primary_reason": "Insufficient data quality and transparency",
            "summary": "This application does not meet the compliance requirements of the EU AI Act due to data quality issues and lack of transparency.",
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
        
        self.trust_factors = {
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
        }
        
        self.recommendations = [
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
        ]
    
    def test_generate_report(self):
        """Test generating a PDF report."""
        # Generate the report
        pdf_data = self.generator.generate_report(
            self.decision_data, self.trust_factors, self.recommendations
        )
        
        # Check that the PDF data is not empty
        self.assertIsInstance(pdf_data, bytes)
        self.assertTrue(len(pdf_data) > 0)
        
        # Check that the PDF starts with the PDF signature
        self.assertTrue(pdf_data.startswith(b'%PDF'))
    
    def test_encode_pdf_to_base64(self):
        """Test encoding PDF data to base64."""
        # Generate a simple PDF
        pdf_data = self.generator.generate_report(
            self.decision_data, self.trust_factors, self.recommendations
        )
        
        # Encode to base64
        base64_data = self.generator.encode_pdf_to_base64(pdf_data)
        
        # Check that the base64 data is a non-empty string
        self.assertIsInstance(base64_data, str)
        self.assertTrue(len(base64_data) > 0)
    
    def test_report_with_custom_logo(self):
        """Test generating a report with a custom logo."""
        # Create a temporary logo file
        logo_path = "/tmp/test_logo.png"
        with open(logo_path, "wb") as f:
            f.write(b"dummy image data")
        
        try:
            # Create a generator with the logo
            generator = ComplianceReportGenerator(logo_path=logo_path)
            
            # Generate the report
            pdf_data = generator.generate_report(
                self.decision_data, self.trust_factors, self.recommendations
            )
            
            # Check that the PDF data is not empty
            self.assertIsInstance(pdf_data, bytes)
            self.assertTrue(len(pdf_data) > 0)
        finally:
            # Clean up the temporary file
            if os.path.exists(logo_path):
                os.remove(logo_path)
    
    def test_report_with_missing_logo(self):
        """Test generating a report with a missing logo file."""
        # Create a generator with a non-existent logo path
        generator = ComplianceReportGenerator(logo_path="/non/existent/path.png")
        
        # Generate the report (should not raise an error)
        pdf_data = generator.generate_report(
            self.decision_data, self.trust_factors, self.recommendations
        )
        
        # Check that the PDF data is not empty
        self.assertIsInstance(pdf_data, bytes)
        self.assertTrue(len(pdf_data) > 0)
    
    def test_report_with_minimal_data(self):
        """Test generating a report with minimal data."""
        # Create minimal data
        minimal_decision = {
            "decision_id": "min_123",
            "application_id": "min_456",
            "is_compliant": True,
            "compliance_score": 85.0,
            "framework": "FINRA"
        }
        
        minimal_trust_factors = {
            "overall_score": 85.0,
            "factors": {}
        }
        
        minimal_recommendations = []
        
        # Generate the report
        pdf_data = self.generator.generate_report(
            minimal_decision, minimal_trust_factors, minimal_recommendations
        )
        
        # Check that the PDF data is not empty
        self.assertIsInstance(pdf_data, bytes)
        self.assertTrue(len(pdf_data) > 0)

if __name__ == "__main__":
    unittest.main()
