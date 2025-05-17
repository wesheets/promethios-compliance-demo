"""
Lending Club API Integration Module

This module provides integration with the Lending Club API to fetch real loan data
for compliance evaluation.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

class LendingClubAPI:
    """
    A class that provides integration with the Lending Club API for fetching loan data.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Lending Club API client.
        
        Args:
            api_key: Lending Club API key. If None, will try to load from environment variable.
            base_url: Base URL for the Lending Club API. If None, will use the default URL.
        """
        self.api_key = api_key or os.environ.get("LENDING_CLUB_API_KEY")
        if not self.api_key:
            raise ValueError("Lending Club API key is required. Set it in the environment as LENDING_CLUB_API_KEY or pass it to the constructor.")
        
        self.base_url = base_url or "https://api.lendingclub.com/api/investor/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_available_loans(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Fetch available loans from Lending Club.
        
        Args:
            limit: Maximum number of loans to fetch
            offset: Offset for pagination
            
        Returns:
            List of loan dictionaries
        """
        try:
            response = requests.get(
                f"{self.base_url}/loans/listing",
                headers=self.headers,
                params={"limit": limit, "offset": offset}
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract loans from the response
            loans = result.get("loans", [])
            
            # Transform loans to match our application format
            transformed_loans = [self._transform_loan(loan) for loan in loans]
            
            return transformed_loans
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching loans from Lending Club: {str(e)}")
            # Return empty list on error
            return []
    
    def get_loan_details(self, loan_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed information for a specific loan.
        
        Args:
            loan_id: ID of the loan to fetch
            
        Returns:
            Loan details dictionary or None if not found
        """
        try:
            response = requests.get(
                f"{self.base_url}/loans/{loan_id}",
                headers=self.headers
            )
            
            response.raise_for_status()
            loan = response.json()
            
            # Transform loan to match our application format
            transformed_loan = self._transform_loan(loan)
            
            return transformed_loan
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching loan details from Lending Club: {str(e)}")
            # Return None on error
            return None
    
    def _transform_loan(self, loan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a Lending Club loan to match our application format.
        
        Args:
            loan: Lending Club loan dictionary
            
        Returns:
            Transformed loan dictionary
        """
        # Extract loan ID or generate one if not present
        loan_id = loan.get("id", f"LC_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Map Lending Club grade to our grade format
        grade_mapping = {
            "A": "A",
            "B": "B",
            "C": "C",
            "D": "C",
            "E": "D",
            "F": "D",
            "G": "E"
        }
        grade = grade_mapping.get(loan.get("grade", ""), "C")
        
        # Map loan purpose to our format
        purpose_mapping = {
            "debt_consolidation": "debt_consolidation",
            "credit_card": "credit_card",
            "home_improvement": "home_improvement",
            "house": "home_improvement",
            "major_purchase": "major_purchase",
            "car": "major_purchase",
            "medical": "medical",
            "moving": "other",
            "vacation": "other",
            "wedding": "other",
            "small_business": "business",
            "other": "other"
        }
        purpose = purpose_mapping.get(loan.get("purpose", "").lower(), "other")
        
        # Transform the loan
        transformed_loan = {
            "application_id": f"LC_{loan_id}",
            "amount": loan.get("loanAmount", 0),
            "purpose": purpose,
            "grade": grade,
            "interest_rate": loan.get("intRate", 0),
            "term": loan.get("term", 36),
            "employment_length": loan.get("empLength", 0),
            "home_ownership": loan.get("homeOwnership", "RENT"),
            "annual_income": loan.get("annualInc", 0),
            "verification_status": loan.get("isIncV", "Not Verified"),
            "dti": loan.get("dti", 0),
            "delinq_2yrs": loan.get("delinq2Yrs", 0),
            "earliest_credit_line": loan.get("earliestCrLine", ""),
            "inq_last_6mths": loan.get("inqLast6Mths", 0),
            "mths_since_last_delinq": loan.get("mthsSinceLastDelinq", None),
            "open_acc": loan.get("openAcc", 0),
            "pub_rec": loan.get("pubRec", 0),
            "revol_bal": loan.get("revolBal", 0),
            "revol_util": loan.get("revolUtil", 0),
            "total_acc": loan.get("totalAcc", 0),
            "initial_list_status": loan.get("initialListStatus", ""),
            "application_type": loan.get("applicationType", "Individual"),
            "addr_state": loan.get("addrState", ""),
            "loan_status": loan.get("loanStatus", "")
        }
        
        return transformed_loan
    
    def mock_loan_data(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate mock loan data for testing when API is not available.
        
        Args:
            count: Number of mock loans to generate
            
        Returns:
            List of mock loan dictionaries
        """
        mock_loans = []
        
        purposes = ["debt_consolidation", "credit_card", "home_improvement", 
                   "major_purchase", "medical", "business", "other"]
        grades = ["A", "B", "C", "D", "E"]
        home_ownership = ["RENT", "MORTGAGE", "OWN"]
        
        for i in range(1, count + 1):
            # Generate a deterministic but varied set of mock loans
            purpose_index = (i % len(purposes))
            grade_index = (i % len(grades))
            ownership_index = (i % len(home_ownership))
            
            # Base amount on the ID with some variation
            amount = 5000 + (i * 2500)
            
            # DTI increases with ID but caps at 35
            dti = min(15 + (i * 2), 35)
            
            # Create the mock loan
            loan = {
                "application_id": f"LC_{1000 + i}",
                "amount": amount,
                "purpose": purposes[purpose_index],
                "grade": grades[grade_index],
                "interest_rate": 5 + (i % 10),
                "term": 36 if i % 2 == 0 else 60,
                "employment_length": min(i, 10),
                "home_ownership": home_ownership[ownership_index],
                "annual_income": 50000 + (i * 5000),
                "verification_status": "Verified" if i % 3 == 0 else "Not Verified",
                "dti": dti,
                "delinq_2yrs": i % 3,
                "earliest_credit_line": f"2010-{i % 12 + 1:02d}-01",
                "inq_last_6mths": i % 5,
                "mths_since_last_delinq": None if i % 4 == 0 else i * 6,
                "open_acc": 3 + (i % 10),
                "pub_rec": i % 2,
                "revol_bal": 10000 + (i * 1000),
                "revol_util": 50 + (i % 30),
                "total_acc": 5 + (i % 15),
                "initial_list_status": "W" if i % 2 == 0 else "F",
                "application_type": "Individual",
                "addr_state": "CA" if i % 5 == 0 else ("NY" if i % 5 == 1 else "TX"),
                "loan_status": "Current" if i % 4 != 0 else "Late"
            }
            
            mock_loans.append(loan)
        
        return mock_loans
