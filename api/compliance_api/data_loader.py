import pandas as pd
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LoanDataLoader:
    def __init__(self, data_path=None):
        # Use environment variable or default
        data_dir = os.getenv("DATA_DIR", "../data")
        self.data_path = data_path or os.path.join(data_dir, "lending_club_sample.csv")
        self._ensure_data_exists()
        
    def _ensure_data_exists(self):
        """Download data if it doesn't exist."""
        if not os.path.exists(self.data_path):
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            # For demo purposes, we'll create a small sample if needed
            if not os.path.exists(self.data_path):
                self._create_sample_data()
    
    def _create_sample_data(self):
        """Create a small sample dataset for demo purposes."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Create sample data
        sample_data = [
            {"id": "LC_1001", "loan_amount": 10000, "interest_rate": 5.32, "grade": "A", "employment_length": 10, "home_ownership": "RENT", "annual_income": 60000, "purpose": "debt_consolidation", "dti": 15.2, "delinq_2yrs": 0},
            {"id": "LC_1002", "loan_amount": 20000, "interest_rate": 10.99, "grade": "C", "employment_length": 3, "home_ownership": "OWN", "annual_income": 75000, "purpose": "home_improvement", "dti": 28.5, "delinq_2yrs": 1},
            {"id": "LC_1003", "loan_amount": 15000, "interest_rate": 7.89, "grade": "B", "employment_length": 5, "home_ownership": "MORTGAGE", "annual_income": 90000, "purpose": "major_purchase", "dti": 18.7, "delinq_2yrs": 0},
            {"id": "LC_1004", "loan_amount": 30000, "interest_rate": 15.23, "grade": "E", "employment_length": 1, "home_ownership": "RENT", "annual_income": 45000, "purpose": "debt_consolidation", "dti": 35.2, "delinq_2yrs": 3},
            {"id": "LC_1005", "loan_amount": 8000, "interest_rate": 6.08, "grade": "A", "employment_length": 8, "home_ownership": "OWN", "annual_income": 120000, "purpose": "credit_card", "dti": 10.1, "delinq_2yrs": 0}
        ]
        
        # Save as CSV
        pd.DataFrame(sample_data).to_csv(self.data_path, index=False)
    
    def load_loan_applications(self, count=5):
        """Load a specified number of loan applications."""
        df = pd.read_csv(self.data_path)
        return df.head(count).to_dict(orient="records")
    
    def get_application_by_id(self, application_id):
        """Get a specific application by ID."""
        df = pd.read_csv(self.data_path)
        application = df[df["id"] == application_id]
        if len(application) == 0:
            return None
        return application.iloc[0].to_dict()
