"""
Unit tests for the Lending Club API integration module.

This module contains tests for the Lending Club API connector and data transformation.
"""

import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
from compliance_api.lending_club_api import LendingClubAPI

class TestLendingClubAPI(unittest.TestCase):
    """Tests for the LendingClubAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the API key
        os.environ["LENDING_CLUB_API_KEY"] = "test_api_key"
        
        # Create the API client
        self.api = LendingClubAPI()
    
    @patch('requests.get')
    def test_get_available_loans(self, mock_get):
        """Test fetching available loans from the API."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "loans": [
                {
                    "id": "123456",
                    "loanAmount": 10000,
                    "purpose": "debt_consolidation",
                    "grade": "A",
                    "intRate": 5.0,
                    "term": 36,
                    "empLength": 5,
                    "homeOwnership": "MORTGAGE",
                    "annualInc": 75000,
                    "isIncV": "Verified",
                    "dti": 15.0,
                    "delinq2Yrs": 0,
                    "earliestCrLine": "2010-01-01",
                    "inqLast6Mths": 1,
                    "mthsSinceLastDelinq": None,
                    "openAcc": 5,
                    "pubRec": 0,
                    "revolBal": 10000,
                    "revolUtil": 30.0,
                    "totalAcc": 10
                },
                {
                    "id": "789012",
                    "loanAmount": 15000,
                    "purpose": "home_improvement",
                    "grade": "B",
                    "intRate": 7.5,
                    "term": 60,
                    "empLength": 3,
                    "homeOwnership": "OWN",
                    "annualInc": 60000,
                    "isIncV": "Not Verified",
                    "dti": 20.0,
                    "delinq2Yrs": 1,
                    "earliestCrLine": "2012-05-15",
                    "inqLast6Mths": 2,
                    "mthsSinceLastDelinq": 24,
                    "openAcc": 4,
                    "pubRec": 0,
                    "revolBal": 8000,
                    "revolUtil": 40.0,
                    "totalAcc": 8
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test the get_available_loans method
        loans = self.api.get_available_loans(limit=2)
        
        # Check that the loans are transformed correctly
        self.assertEqual(len(loans), 2)
        
        # Check the first loan
        self.assertEqual(loans[0]["application_id"], "LC_123456")
        self.assertEqual(loans[0]["amount"], 10000)
        self.assertEqual(loans[0]["purpose"], "debt_consolidation")
        self.assertEqual(loans[0]["grade"], "A")
        
        # Check the second loan
        self.assertEqual(loans[1]["application_id"], "LC_789012")
        self.assertEqual(loans[1]["amount"], 15000)
        self.assertEqual(loans[1]["purpose"], "home_improvement")
        self.assertEqual(loans[1]["grade"], "B")
        
        # Check that the API was called with the correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        self.assertEqual(call_args["headers"]["Authorization"], "Bearer test_api_key")
        self.assertEqual(call_args["params"]["limit"], 2)
    
    @patch('requests.get')
    def test_get_loan_details(self, mock_get):
        """Test fetching details for a specific loan."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "123456",
            "loanAmount": 10000,
            "purpose": "debt_consolidation",
            "grade": "A",
            "intRate": 5.0,
            "term": 36,
            "empLength": 5,
            "homeOwnership": "MORTGAGE",
            "annualInc": 75000,
            "isIncV": "Verified",
            "dti": 15.0,
            "delinq2Yrs": 0,
            "earliestCrLine": "2010-01-01",
            "inqLast6Mths": 1,
            "mthsSinceLastDelinq": None,
            "openAcc": 5,
            "pubRec": 0,
            "revolBal": 10000,
            "revolUtil": 30.0,
            "totalAcc": 10
        }
        mock_get.return_value = mock_response
        
        # Test the get_loan_details method
        loan = self.api.get_loan_details("123456")
        
        # Check that the loan is transformed correctly
        self.assertEqual(loan["application_id"], "LC_123456")
        self.assertEqual(loan["amount"], 10000)
        self.assertEqual(loan["purpose"], "debt_consolidation")
        self.assertEqual(loan["grade"], "A")
        
        # Check that the API was called with the correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        self.assertEqual(call_args["headers"]["Authorization"], "Bearer test_api_key")
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test handling of API errors."""
        # Mock an API error
        mock_get.side_effect = Exception("API error")
        
        # Test the get_available_loans method with the error
        loans = self.api.get_available_loans()
        
        # Check that an empty list is returned
        self.assertEqual(loans, [])
    
    def test_missing_api_key(self):
        """Test handling of missing API key."""
        # Remove the API key from environment
        if "LENDING_CLUB_API_KEY" in os.environ:
            del os.environ["LENDING_CLUB_API_KEY"]
        
        # Check that creating an API client without an API key raises an error
        with self.assertRaises(ValueError):
            LendingClubAPI()
    
    def test_transform_loan(self):
        """Test the loan transformation logic."""
        # Sample Lending Club loan data
        lc_loan = {
            "id": "123456",
            "loanAmount": 10000,
            "purpose": "debt_consolidation",
            "grade": "A",
            "intRate": 5.0,
            "term": 36,
            "empLength": 5,
            "homeOwnership": "MORTGAGE",
            "annualInc": 75000,
            "isIncV": "Verified",
            "dti": 15.0,
            "delinq2Yrs": 0,
            "earliestCrLine": "2010-01-01",
            "inqLast6Mths": 1,
            "mthsSinceLastDelinq": None,
            "openAcc": 5,
            "pubRec": 0,
            "revolBal": 10000,
            "revolUtil": 30.0,
            "totalAcc": 10
        }
        
        # Transform the loan
        transformed = self.api._transform_loan(lc_loan)
        
        # Check that the transformation is correct
        self.assertEqual(transformed["application_id"], "LC_123456")
        self.assertEqual(transformed["amount"], 10000)
        self.assertEqual(transformed["purpose"], "debt_consolidation")
        self.assertEqual(transformed["grade"], "A")
        self.assertEqual(transformed["interest_rate"], 5.0)
        self.assertEqual(transformed["term"], 36)
        self.assertEqual(transformed["employment_length"], 5)
        self.assertEqual(transformed["home_ownership"], "MORTGAGE")
        self.assertEqual(transformed["annual_income"], 75000)
        self.assertEqual(transformed["verification_status"], "Verified")
        self.assertEqual(transformed["dti"], 15.0)
        self.assertEqual(transformed["delinq_2yrs"], 0)
        self.assertEqual(transformed["earliest_credit_line"], "2010-01-01")
        self.assertEqual(transformed["inq_last_6mths"], 1)
        self.assertEqual(transformed["mths_since_last_delinq"], None)
        self.assertEqual(transformed["open_acc"], 5)
        self.assertEqual(transformed["pub_rec"], 0)
        self.assertEqual(transformed["revol_bal"], 10000)
        self.assertEqual(transformed["revol_util"], 30.0)
        self.assertEqual(transformed["total_acc"], 10)
    
    def test_transform_loan_with_missing_fields(self):
        """Test transforming a loan with missing fields."""
        # Sample Lending Club loan data with missing fields
        lc_loan = {
            "id": "123456",
            "loanAmount": 10000,
            "purpose": "debt_consolidation"
            # Many fields missing
        }
        
        # Transform the loan
        transformed = self.api._transform_loan(lc_loan)
        
        # Check that the transformation handles missing fields gracefully
        self.assertEqual(transformed["application_id"], "LC_123456")
        self.assertEqual(transformed["amount"], 10000)
        self.assertEqual(transformed["purpose"], "debt_consolidation")
        self.assertEqual(transformed["grade"], "C")  # Default grade
        self.assertEqual(transformed["interest_rate"], 0)  # Default value
    
    def test_mock_loan_data(self):
        """Test generating mock loan data."""
        # Generate mock loans
        mock_loans = self.api.mock_loan_data(count=5)
        
        # Check that the correct number of loans is generated
        self.assertEqual(len(mock_loans), 5)
        
        # Check that each loan has the expected fields
        for loan in mock_loans:
            self.assertIn("application_id", loan)
            self.assertIn("amount", loan)
            self.assertIn("purpose", loan)
            self.assertIn("grade", loan)
            self.assertIn("interest_rate", loan)
            self.assertIn("term", loan)
            self.assertIn("employment_length", loan)
            self.assertIn("home_ownership", loan)
            self.assertIn("annual_income", loan)
            self.assertIn("verification_status", loan)
            self.assertIn("dti", loan)
            self.assertIn("delinq_2yrs", loan)
            self.assertIn("earliest_credit_line", loan)
            self.assertIn("inq_last_6mths", loan)
            self.assertIn("mths_since_last_delinq", loan)
            self.assertIn("open_acc", loan)
            self.assertIn("pub_rec", loan)
            self.assertIn("revol_bal", loan)
            self.assertIn("revol_util", loan)
            self.assertIn("total_acc", loan)

if __name__ == "__main__":
    unittest.main()
